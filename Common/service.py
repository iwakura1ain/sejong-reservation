import mariadb

import requests
import requests.exceptions

#from sqlalchemy import create_engine


class Service:
    def __init__(self, *args, **kwargs):
        db_config = kwargs["db_config"]
        model_config = kwargs["model_config"]
        api_config = kwargs["api_config"]

        if db_config is not None:
            print("db config: ", db_config)
            self.db_config = db_config
            self.db = mariadb.connect(**db_config)
            self.cur = self.db.cursor()

        if model_config is not None:
            self.engine = None
            self.model = None

        if api_config is not None:
            self.api_config = api_config
            self.api = api_config

    def query_model(self, fuction):
        raise NotImplementedError
        
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

        #url = self.api[api_name]["url"].format(**request_args) -> for url endpoints such as example.com/api/room/1/users/4

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



    

