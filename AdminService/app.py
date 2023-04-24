from flask import Flask, request
import os
import admin

app = Flask(__name__)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 