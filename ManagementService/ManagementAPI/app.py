from flask import Flask, request
from flask_restx import Api
import managementservice
import os

from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

api.add_namespace(managementservice.management, '/management/rooms')


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=5000) 

    # when running local
    # app.run(host="0.0.0.0", debug=True, port=5005)    

# /rooms/<id>: get <id> room
