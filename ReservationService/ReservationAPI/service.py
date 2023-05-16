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
    This is a Python decorator function that registers validation functions.
    
    :param key: The key parameter is a string that represents the validation function's target. It is
    used to register the validation function in a global dictionary called VALIDATORS.
    
    :return: The `validator` function returns the inner `decorator_register` function, which is used to
    register the decorated validation function in a global dictionary `VALIDATORS` with the specified
    `key`.

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
    This is a validator method for a request body in a SQLAlchemy model that validates the data and
    returns a dictionary of validated values mapped to the model.
    
    :param data: The parameter `data` is a JSON dictionary that represents the request body. It contains
    key-value pairs that correspond to the fields and values of the model that the validator is being
    applied to.
    
    :return: The method is returning a dictionary of validated values mapped to the model.
    
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


"""
The Service class is a helper class for making database and API queries, with methods for querying
SQL databases, ORM databases, and APIs.
"""
class Service:
    def __init__(self, *args, **kwargs):
        """
        This is a constructor function for a class that initializes database, ORM, and API
        configurations based on the arguments passed to it.
        
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
        """
        This function initializes the ORM engine and base for a given model configuration.
        
        :param model_config: It is a dictionary containing the configuration parameters for the ORM
        (Object-Relational Mapping) engine. These parameters include the database connection details
        such as the host, port, username, password, and database name.
        
        :return: If `ORM_BASE` and `ORM_ENGINE` are not `None`, the function returns without doing
        anything. Otherwise, it initializes the ORM engine and base by creating an engine using the
        `create_engine` function from SQLAlchemy and preparing the base using the `automap_base`
        function from SQLAlchemy.
        """
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
        """
        This function initializes a model by creating a dictionary of tables and their corresponding
        columns.
        
        :param tables: The `tables` parameter is a list of table names that the function will use to
        initialize the model.
        
        :return: a dictionary containing the ORM classes for each table in the input `tables` list. The
        keys of the dictionary are the table names and the values are the corresponding ORM classes.
        Each ORM class also has a `columns` attribute which is a list of strings representing the column
        names for that table.
        """
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
        This is a context manager function used for ORM database queries in Python.
        
        :param model_name: The name of the table in the ORM database that you want to query.

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
        This is a method used for SQL database queries that takes a query, arguments, and a boolean
        value indicating whether the query is a SELECT statement or not, and returns the results of the
        query or True/False depending on the value of the boolean.
        
        :param query: The SQL query to be executed on the database.
        
        :param args: args is a tuple of arguments to be passed to the SQL query. These arguments are
        used to replace placeholders in the query string. For example, if the query string contains a
        placeholder '%s', the first element of the args tuple will replace it.
        
        :param retval: The parameter `retval` is a boolean flag that indicates whether the SQL query is
        a SELECT statement or not. If `retval` is True, it means that the query is a SELECT statement
        and the method should return the result set of the query. If `retval` is False, it means that,
        defaults to False (optional).
        
        :return: The method returns either the result of the SQL query (if `retval` is True and the
        query is a SELECT statement) or a boolean value indicating whether the query was successful (if
        `retval` is False and the query is not a SELECT statement). If there is an error, it returns an
        empty list (if `retval` is True) or False (if `retval` is False).

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

        
    def query_api(self, api_name, request_method, request_params={}, headers=None, body=None):
        """
        This function is used for making API queries with specified parameters and returns the response
        in JSON format.
        
        :param api_name: The name of the API that is registered in the `api_config` dictionary.
        
        :param request_method: The HTTP request method to be used for the API query. It can be "get",
        "post", "put", or "delete"
        
        :param request_params: Request parameters are additional data that can be sent along with the
        API request. These parameters are usually used to filter or sort the data that is returned by
        the API. For example, if you are querying a list of products, you might use request parameters
        to filter the results by category or price range.
        
        :param headers: Headers are additional information that can be sent along with a request to
        provide more context or authentication. They typically include key-value pairs such as
        authorization tokens, content type, and user agent. In the given code, headers are an optional
        parameter that can be passed to the `query_api` method to include.

        :param body: The request body is the data that is sent as part of the HTTP request. It can
        contain information such as form data, JSON data, or XML data. The body parameter in the
        query_api function is used to pass this data to the API endpoint being queried.
        
        :return: the JSON response obtained from making an API query using the specified API name,
        request method, request parameters, headers, and body. If an error occurs during the API query,
        the function returns False.

        ---
        api_name: registered api name in api_config
        request_method: "get", "post", "put", "delete"
        request_params: request parameters
        headers: request headers
        body: request body

        ---
        USAGE:
        api_config = {
        "api_name1": "http:api1:5000/path/to/api",
        "api_name2": "http:api2:5000/path/to/api",
        }
        """

        if self.api_config is None:
            raise NotImplementedError

        # for url endpoints such as example.com/api/room/1/users/4
        #url = self.api[api_name]["url"].format(**request_params)
        url = self.api_config[api_name].format(**request_params)

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



    

