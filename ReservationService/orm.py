from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect

import pymysql

class sampleORM():
    """ 
    sqlalchemy testing. 
    not final. 
    """

    def __init__(self):
        self.Base = automap_base()
        self.engine = self.init_engine()
        self.table_names = inspect(self.engine).get_table_names()
        self.tables = self.create_tables()

    def init_engine(self):
        url_object = URL.create(
            #"mariadb+pymysql",
            "mysql+mysqlconnector",
            username = "testusr",password = "1234",
            host = "db-service",
            database = "exampledb",
            port = 3306,
        )
        _engine = create_engine(url_object,echo=True)
        self.Base.prepare(_engine)
        return _engine
    
    def create_tables(self):
        _tables = {}
        for name in self.table_names:
            t = Table(name, MetaData(), 
                autoload_with=self.engine)
            _tables[name] = {}
            #_tables[name]["table"] = t
            _tables[name]["schema"] = t.schema
            _tables[name]["description"] = t.description
            _tables[name]["columns"] = t.columns.values()
            _tables[name]["indexes"] = t.indexes
            _tables[name]["key"] = t.key
            _tables[name]["primary_key"] = t.primary_key
            _tables[name]["foreign_keys"] = t.foreign_keys
            _tables[name]["foreign_key_constraints"] = t.foreign_key_constraints
            _tables[name]["foreign_keys"] = t.foreign_keys
            _tables[name]["info"] = t.info
        return _tables
