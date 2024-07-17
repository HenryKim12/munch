from flask import Blueprint, request, jsonify
from app.extensions import db
from dotenv import load_dotenv
from app import models, services

import os

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/users', methods=["GET"])
def get():
    try:
        users = services.get_users()
        return jsonify(users), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400
    

@main.route('/users/<int:id>', methods=["GET"])
def getByID(id):
    try:
        user = services.get_user_by_id(id)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400

@main.route('/users/<int:id>', methods=["DELETE"])
def delete(id):
    try:
        services.delete_user(id)
        return jsonify(f"Successfully deleted user {id}"), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/users', methods=["POST"])
def post():
    try:
        data = request.get_json()
        services.create_user(data)
        return jsonify(f"Successfully added new user"), 200
    except ValueError as e:
        return jsonify(str(e)), 409
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/users/<int:id>', methods=["PUT"])
def update(id):
    try:
        data = request.get_json()
        services.update_user(id, data)
        return jsonify(f"Successfully update user {id}"), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        return jsonify(str(e)), 400