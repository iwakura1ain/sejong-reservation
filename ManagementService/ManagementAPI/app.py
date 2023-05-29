from flask import Flask, request
from flask_restx import Api
from managementservice import management
import os

from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    api = Api(app)
    api.add_namespace(management, '/admin')

    CORS(app)

    return app, api

APP, API = create_app()

if __name__=="__main__":
    APP.run(host="0.0.0.0", debug=True, port=5000) 

    # when running local
    # app.run(host="0.0.0.0", debug=True, port=5005)    

# /rooms/<id>: get <id> room
