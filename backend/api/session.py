from flask import Blueprint, request, jsonify
from flask_cors import CORS
from api.utils import expect
from datetime import datetime
from bson import ObjectId
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from flask import current_app, g


sessions_api_v1 = Blueprint(
    'sessions_api_v1', 'sessions_api_v1', url_prefix='/api/v1/sessions')

CORS(sessions_api_v1)


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


# Create a new session
@sessions_api_v1.route('/sessions', methods=['POST'])
def create_session():
    try:
        data = request.json
        collection = db.sessions
        result = collection.insert_one(data)
        inserted_id = result.inserted_id
        return jsonify({"message": "Session created successfully", "id": str(inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)})

# Read sessions by userID


@sessions_api_v1.route('/sessions/<string:user_id>', methods=['GET'])
def read_sessions(user_id):
    try:
        collection = db.sessions
        sessions = list(collection.find({"userID": user_id}))
        return jsonify(sessions)
    except Exception as e:
        return jsonify({"error": str(e)})

# Read a session by ID


@sessions_api_v1.route('/sessions/<string:id>', methods=['GET'])
def read_session(id):
    try:
        collection = db.sessions
        session = collection.find_one({"_id": ObjectId(id)})
        if session:
            return jsonify(session)
        else:
            return jsonify({"message": "Session not found"})
    except Exception as e:
        return jsonify({"error": str(e)})


@sessions_api_v1.route('/sessions/<string:id>', methods=['PUT'])
def update_session(id):
    try:
        data = request.json
        collection = db.sessions
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Session updated successfully"})
        else:
            return jsonify({"message": "Session not found or not updated"})
    except Exception as e:
        return jsonify({"error": str(e)})


@sessions_api_v1.route('/sessions/<string:id>', methods=['PUT'])
def delete_session(id):
    try:
        collection = db.sessions
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Session deleted successfully"})
        else:
            return jsonify({"message": "Session not found or not deleted"})
    except Exception as e:
        return jsonify({"error": str(e)})
