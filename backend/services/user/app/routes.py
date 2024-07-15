from flask import Blueprint, request, jsonify
from app.extensions import db
import os
from dotenv import load_dotenv
from . import models, services

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/users', methods=["GET"])
def get():
    try:
        users = services.get_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify(str(e)), 400
    

@main.route('/users/<int:id>', methods=["GET"])
def getByID():
    try:
        user = services.get_user_by_id(request.args.get("id"))
        return jsonify(user), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/users/<int:id>', methods=["DELETE"])
def delete():
    try:
        services.delete_user(request.args.get("id"))
        return jsonify(f"Successfully deleted user {request.args.get("id")}"), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/users', methods=["POST"])
def post():
    try:
        data = request.get_json()
        services.create_user(data)
        return jsonify(f"Successfully added new user"), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/users/<int:id>', methods=["PUT"])
def update():
    try:
        data = request.get_json()
        services.update_user(request.args.get("id"), data)
        return jsonify(f"Successfully update user {request.args.get("id")}"), 200
    except Exception as e:
        return jsonify(str(e)), 400