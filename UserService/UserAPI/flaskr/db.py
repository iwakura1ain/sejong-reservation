import flask
import json
import mariadb

import click
from flask import current_app, g

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'testusr2',
    'password': '1234',
    'database': 'exampledb2',
    'autocommit': True
}


def get_db():
    
    # cur.execute("select * from people")
    # # serialize results into JSON
    # row_headers=[x[0] for x in cur.description]
    # rv = cur.fetchall()
    # json_data=[]
    # for result in rv:
    #     json_data.append(dict(zip(row_headers,result)))
    
    # # return the results!
    # return json.dumps(json_data)
    
    if 'db' not in g:
        g.db = mariadb.connect(**config)
    return g.db

def get_cur():
    if 'cur' not in g:
        g.cur = get_db().cursor()

    return g.cur


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
        
def init_db():
    cur = get_db()
    # with current_app.open_resource('schema.sql') as f:
    #     cur.execute(f.read().decode('utf8'))

    # fd = open(filename, 'r')
    # sqlFile = fd.read()
    # fd.close()
    # sqlCommands = sqlFile.split(';')

    # for command in sqlCommands:
    #     try:
    #         if command.strip() != '':
    #             cursor.execute(command)
    #     except IOError, msg:
    #         print "Command skipped: ", msg

    with current_app.open_resource("schema.sql") as f:
        sqlFile = f.read().decode("utf-8")
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            try:
                
                cur.execute(command)
            except Exception as e:
                print(e)




@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
