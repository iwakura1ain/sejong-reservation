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

<<<<<<< HEAD
=======
# app.add_url_rule("/upload/<name>", endpoint="download_file", build_only=True)
>>>>>>> 09dad8734fb9b4d80e172b6bc806f90fcdb514f6
api.add_namespace(adminservice.admin, '/admin/rooms')

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=5005) 

# /rooms/<id>: get <id> room
