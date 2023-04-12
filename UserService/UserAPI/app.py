from flask import Flask
from flask_restx import Resource, Api, Namespace
from flask_jwt_extended import JWTManager

from auth import auth
import os
import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["JWT_SECRET_KEY"] = "DEVELOPMENT-KEY-MUST-CHANGE"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # connect db and init
    db.init_app(app)

    return app


app = create_app()

api = Api(app)
api.add_namespace(auth, '/auth')  # add endpoints from auth.py

jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
