from flask import Flask
from flask_restx import Resource, Api, Namespace

from flask_jwt_extended import JWTManager, exceptions
from flask_cors import CORS

import os
from datetime import timedelta

import auth
import users


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)#, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = "3d6f45a5fc12445dbac2f59c3b6c7cb1"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    CORS(app)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # connect test db and init
    #db.init_app(app)

    api = Api(app)
    api.add_namespace(auth.AUTH, '/auth')  # add endpoints from auth.py
    api.add_namespace(users.USERS, '/users')  # add endpoints from users.py

    jwt = JWTManager(app)
    #jwt._set_error_handler_callbacks(api)

    return app, api, jwt

APP, API, JWT = create_app()

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

        if res is not None:
            return True
        
        return False

class CustomRevokedTokenError(exceptions.JWTExtendedException):
    """
    Error raised when a revoked token attempt to access a protected endpoint
    """

    def __init__(self, jwt_header: dict, jwt_data: dict) -> None:
        super().__init__("Token has been revoked")
        self.jwt_header = jwt_header
        self.jwt_data = jwt_data
        
if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=5000)



