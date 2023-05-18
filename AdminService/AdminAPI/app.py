from flask import Flask, request
from flask_restx import Api
import adminservice
import os

app = Flask(__name__)
api = Api(app)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

api.add_namespace(adminservice.admin, '')
api.add_namespace(adminservice.admin, '<int:id>')

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=8002) 

# /rooms/<id>: get <id> room
