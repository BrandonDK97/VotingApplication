import configparser
import os

from flask import Flask, render_template
from json import JSONEncoder
from flask_cors import CORS
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended import JWTManager
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini')))


from bson import json_util, ObjectId
from datetime import datetime, timedelta

from api.session import sessions_api_v1

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():

    app = Flask(__name__)

    # Allow CORS (Cross-Origin Resource Sharing)
    CORS(app)

    app.json_encoder = MongoJsonEncoder
    app.register_blueprint(sessions_api_v1)

    return app

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['PROD']['DB_URI']
    app.run(host='0.0.0.0', port=5000)