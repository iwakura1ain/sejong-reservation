from flask import Flask
from flask_restx import Resource, Api
from auth import Auth

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="API auth test",
    description="API auth test",
    terms_url="/",
    contact="",
    license="GPL3"
)

api.add_namespace(Auth, '/auth')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
