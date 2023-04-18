import mariadb

import requests
import requests.exceptions

from sqlalchemy import (
    create_engine,
    inspect,
    MetaData,
    Table,
    URL
)
from sqlalchemy.orm import create_session
from sqlalchemy.ext.automap import automap_base

# model_config = {
#     username="testusr",
#     password="1234",
#     host="db-service",
#     database="exampledb",
#     port=3306,
# }

class Service:
    def __init__(self, *args, **kwargs):
        db_config = kwargs["db_config"]
        model_config = kwargs["model_config"]
        api_config = kwargs["api_config"]

        if db_config is not None:
            self.db_config = db_config
            self.db = mariadb.connect(**db_config)
            self.cur = self.db.cursor()

        if model_config is not None:
            self.model_config = model_config
            self.base = automap_base()
            self.engine = self.init_orm_engine(model_config)

            self.table_names = inspect(self.engine).get_table_names()
            self.models = {
                n: Table(n, MetaData(), autoload_with=self.engine)
                for n in self.table_names
            }

        if api_config is not None:
            self.api_config = api_config
            self.api = api_config
            
            
    def init_orm_engine(self, model_config):
        db_object = URL.create(
            "mysql+mysqlconnector",
            **model_config
        )
        _engine = create_engine(db_object, echo=True)
        self.base.prepare(_engine)
        return _engine

    
    def query_model(self, table):
        if self.model_config is None:
            raise NotImplementedError

        return self.model.get(table)

    
    def query_db(self, query, args=(), retval=False):
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
            return None if retval else False

        except Exception as e:  # TODO: differnet exceptions for invalid cursors etc
            raise e

        
    def query_api(self, api_name, request_method, request_params=None, headers=None, body=None):
        """
        {
        'api_name1': {'url': 'example.com:9999/api/api1'},
        'api_name2': {'url': 'example.com:9999/api/api2'}
        }
        """

        if self.api_config is None:
            raise NotImplementedError

        # for url endpoints such as example.com/api/room/1/users/4
        # url = self.api[api_name]["url"].format(**request_args) 

        try:
            req = getattr(requests, request_method)
            res = req(
                self.api[api_name]["url"],
                headers=headers,
                params=request_params,
                data=body
            )
            return res.json() # will raise error if response is not jsn

        except Exception as e:
            return False



    

