from flask import Flask
from flask_restx import Resource, Api, Namespace
from flask_jwt_extended import JWTManager

from auth import auth
from users import users

import os
from datetime import timedelta


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

    return app


app = create_app()

api = Api(app)
api.add_namespace(auth, '/auth')  # add endpoints from auth.py
api.add_namespace(users, '/users')  # add endpoints from users.py

jwt = JWTManager(app)


# IMPORTANT!!!
# TODO: change to db
TOKEN_BLOCKLIST = []

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    global TOKEN_BLOCKLIST
    jti = jwt_payload["jti"]
    
    return True if jti in TOKEN_BLOCKLIST else False

def add_token_to_blocklist(jti):
    global TOKEN_BLOCKLIST
    TOKEN_BLOCKLIST.append(jti)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
