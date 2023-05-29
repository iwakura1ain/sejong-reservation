from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS

from service import Service
import reservation
import checkin

def create_app():
    

    app = Flask(__name__)
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list' # none, list, full
    CORS(app)

    api = Api(app)
    api.add_namespace(reservation.ns, "/reservation")
    api.add_namespace(checkin.CHECK_IN, '/check-in')

    return app, api

APP, API = create_app()

if __name__=="__main__":
    APP.run(host="0.0.0.0", port=5000, debug=True)


