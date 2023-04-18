from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, Session
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect

from fastapi import APIRouter, Depends

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
            _tables[name] = t
        return _tables

router = APIRouter(prefix="/ormtest")

def get_orm():
    "returns new sampleORM object"
    yield sampleORM()

@router.get("/info")
def get_all_tables(myorm=Depends(get_orm)):
    """
    get info for all tables in database
    """
    # sqlalchemy objects are NOT compatible with JSONResponse
    # return str(myorm.tables['User']) 
    # return [{k:str(v.columns.values())} for k,v in myorm.tables.items()]
    return [
        {k: {
            "type": str(type(v)),
            "columns": [str(c) for c in v.columns.values()],
            "indexes": [str(c) for c in v.columns.values()],
            "key": str(v.key),
            "primary_key": str(v.primary_key),
            "foreign_keys": [str(c) for c in v.foreign_keys],
            "foreign_key_constraints": [str(c) for c in v.foreign_key_constraints],
            "indexes":str(v.indexes),
        }} for k, v in myorm.tables.items()]
