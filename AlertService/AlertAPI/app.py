from flask import Flask
from flask_restx import Api

import os
from datetime import timedelta

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app, api

APP, API = create_app()

if __name__ == "__main__":
    import alert
    
    API.add_namespace(alert.EMAIL, '/alert')
    APP.run(debug=True, host='0.0.0.0', port=5000)
