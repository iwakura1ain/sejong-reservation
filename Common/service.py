import mariadb

import requests
import requests.exceptions

from sqlalchemy import (
    event,
    create_engine,
    inspect,
    MetaData,
    Table,
    URL
)
from sqlalchemy.orm import create_session, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from contextlib import contextmanager

# sqlalchemy objects
ORM_BASE = None
ORM_ENGINE = None

# registered validation functions
VALIDATORS = {}

def validator(key):
    """
    Decorator which decorates validation functions.
    ---
    USAGE:
    @validator("Reservation.date")
    def reservation_date_validator(val):  # example validator
        if cond:
            return True
        return False
    """
    def decorator_register(func):
        global VALIDATORS
        VALIDATORS[key] = func
        return func
    return decorator_register


def validate(self, data):
    """
    Validator method for request body. Injected into sqlalchemy Model.
    ---
    USAGE:
    with self.query_model(<TABLE NAME>) as (conn, <TABLE>):
        verified_json_body = <TABLE>.validate(<REQUEST BODY>)
    ---
    data: json dict
    ---
    Returns dict of validated values mapped to model.
    """
    retval = {}
    for key, val in data.items():
        schema_key = f"{self.__name__}.{key}"
        if schema_key not in self.columns:
            continue
        
        default_validator = VALIDATORS.get(self.__name__)
        if default_validator is not None and default_validator(val) is False:
            continue
        
        key_validator = VALIDATORS.get(schema_key)
        if key_validator is not None and key_validator(val) is False:
            continue
        
        retval[key] = val
            
    return retval
# inject validate function into sqlalchemy
DeclarativeMeta.validate = validate


class Service:
    def __init__(self, *args, **kwargs):
        """
        Class inherited by all services. Used for database, api queries.
        ---
        db_config: sql query config
        model_config: orm query config
        api_config: api query config
        """
        
        db_config = kwargs.get("db_config")
        # db_config = {
        #     'host': '127.0.0.1',
        #     'port': 3306,
        #     'user': 'testusr2',
        #     'password': '1234',
        #     'database': 'test1',
        #     'autocommit': True
        # }

        model_config = kwargs.get("model_config")
        # model_config = {
        #     username="testusr",
        #     password="1234",
        #     host="db-service",
        #     database="exampledb",
        #     port=3306,
        # }

        api_config = kwargs.get("api_config")
        # api_config = {
        #     "api_name1": "http://api1:5000/api/endpoint",
        #     "api_name2": "http://api2:5000/api/endpoint"
        # }

        if db_config is not None:
            self.db_config = db_config
            self.db = mariadb.connect(**db_config)
            self.cur = self.db.cursor()

        if model_config is not None:
            self.init_orm(model_config)
            self.model_config = model_config
            self.connection = ORM_ENGINE.connect()
            self.session = sessionmaker(ORM_ENGINE)

            self.tables = inspect(ORM_ENGINE).get_table_names()
            self.models = self.init_model(self.tables)
            
        if api_config is not None:
            self.api_config = api_config
            self.api = api_config
            

    @staticmethod
    def init_orm(model_config):
        global ORM_ENGINE, ORM_BASE

        if ORM_BASE is not None or ORM_ENGINE is not None:
            return

        ORM_ENGINE = create_engine(
            URL.create(
                #"mysql+mysqlconnector",
                "mariadb+pymysql",
                **model_config        
            )
        )

        ORM_BASE = automap_base()
        ORM_BASE.prepare(autoload_with=ORM_ENGINE, reflect=True)

    
    def init_model(self, tables):
        global VALIDATORS
        
        retval = {}
        for t in self.tables:
            if t in dir(ORM_BASE.classes):
                retval[t] = getattr(ORM_BASE.classes, t)
                setattr(
                    retval[t],
                    "columns",
                    [str(c) for c in retval[t].__table__.c]
                )

        return retval

    
    @contextmanager
    def query_model(self, model_name):
        """
        Method used for orm database queries
        ---
        USAGE:
        with self.query_model(<TABLE NAME>) as (conn, <TABLE>):
            res = conn.execute(...)
        ---
        model_name: table name
        """
        if self.model_config is None:
            raise NotImplementedError

        try:
            model = self.models[model_name]
            yield (self.connection, model)
            self.connection.commit()

        except Exception as e:
            raise e
        
    
    def query_db(self, query, args=(), retval=False):
        """
        method used for sql database queries
        ---
        query: sql query
        args: sql query arguments
        retval: True for SELECT | FALSE for INSERT, DELETE, etc
        """
        if self.db_config is None:
            raise NotImplementedError
        
        try:
            self.cur.execute(query, args,)
            # if retval := self.cur.fetchall() is not None:
            #     return retval
            # return True
            return self.cur.fetchall() if retval else True

        except mariadb.Error as e:
            print(f"db error: {e}")
            return [] if retval else False

        except Exception as e:  # TODO: differnet exceptions for invalid cursors etc
            raise e

        
    def query_api(self, api_name, request_method, request_params=None, headers=None, body=None):
        """
        method used for api queries
        ---
        api_name: registered api name in api_config
        request_method: "get", "post", "put", "delete"
        request_params: request parameters
        headers: request headers
        body: request body
        """

        if self.api_config is None:
            raise NotImplementedError

        # for url endpoints such as example.com/api/room/1/users/4
        #url = self.api[api_name]["url"].format(**request_params)
        url = self.api[api_name].format(**request_params)

        try:
            req = getattr(requests, request_method)
            res = req(
                #self.api[api_name]["url"],
                url,
                headers=headers,
                params=request_params,
                data=body
            )
            return res.json() # will raise error if response is not jsn

        except Exception as e:
            return False



    

