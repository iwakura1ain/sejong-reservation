from flask import Flask
from flask_restx import Api

from flask_cors import CORS

import os
from datetime import timedelta

import alert

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    api = Api(app)
    api.add_namespace(alert.EMAIL, '/alert')

    CORS(app)

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    return app, api

APP, API = create_app()

if __name__=="__main__":
    APP.run(debug=True, host='0.0.0.0', port=5000)
