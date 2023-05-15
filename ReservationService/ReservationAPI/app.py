from flask import Flask
from flask_restx import Resource, Api

from service import Service
import reservation

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list' # none, list, full

api = Api(app)
api.add_namespace(reservation.ns)
app.run(host="0.0.0.0", port=5555, debug=True)