from flask import Flask
from flask_restx import Resource, Api, Namespace

# from auth import auth
# from users import users

import os
from datetime import timedelta

from flask_jwt_extended import JWTManager

import auth
import users


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = "DEVELOPMENT-KEY-MUST-CHANGE"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # connect test db and init
    #db.init_app(app)

    api = Api(app)

    return app, api

APP, API = create_app()
JWT = JWTManager(APP)

@JWT.token_in_blocklist_loader # Callback function to check if a JWT exists in the database blocklist
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Will run for every request and check if token is revoked
    """
    
    from service import Service
    from config import ORM
    from sqlalchemy import select

    service = Service(model_config=ORM)
    with service.query_model("Token_Blocklist") as (conn, Blocklist):
        res = conn.execute(
            select(Blocklist).where(Blocklist.jti == jwt_payload["jti"])
        ).mappings().fetchone()

        return False if res is None else True

if __name__ == "__main__":    
    API.add_namespace(auth.AUTH, '/auth')  # add endpoints from auth.py
    API.add_namespace(users.USERS, '/users')  # add endpoints from users.py
    APP.run(debug=True, host='0.0.0.0', port=5000)
