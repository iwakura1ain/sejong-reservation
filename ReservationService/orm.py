from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy import URL
from sqlalchemy.ext.automap import automap_base

import pymysql

class DB(): 
    def __init__(self):
        self.db = pymysql.connect(
                host='db-service',
                port=3306,
                user='testusr',
                password='1234',
                database='exampledb',
        )

    def get_cur(self):
        return self.db.cursor()

    def close_db(self):
        self.db.close()

# db = DB()
# print(db)
# cur = get_cur()
# cur.query("select * from reservation")
# resp = cur.fetchall()
# print(resp)

Base = automap_base()
def get_session():
    # full_url = f"mysql+mysqlconnector://{user}:{pw}@{docker_name}:{port}/{databasename}?charset=utf8mb4"
    url_object = URL.create(
        #"mariadb+pymysql",
        "mysql+mysqlconnector",
        username = "testusr",password = "1234",
        host = "db-service",
        database = "exampledb",
        port = 3306,
    )
    #Base.metadata.create_all(bind=engine)
    #return sessionmaker(bind=engine)

    engine = create_engine(url_object,echo=True)
    Base.prepare(engine)
    return create_session(bind=engine)


def get_tables():
    session = get_session()
    print(session)

    """
    for table in [User,Room]:
        print(table)
        print([c for c in table.columns])
        exec = select(table) # == exec = table.select()
        for x in session.execute(exec):
            print(x)
    """


