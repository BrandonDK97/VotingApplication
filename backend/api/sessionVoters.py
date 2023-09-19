from flask import Blueprint, request, jsonify
from flask_cors import CORS
from api.utils import expect
from datetime import datetime
from flask_pymongo import PyMongo
from bson import ObjectId


sessionVoters_api_v1 = Blueprint(
    'sessionVoters_api_v1', 'sessionVoters_api_v1', url_prefix='/api/v1/sessionVoters')

CORS(sessionVoters_api_v1)

mongo = PyMongo()

