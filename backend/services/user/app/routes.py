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
    
@main.route("/users/<int:user_id>/restaurants", methods=["GET"])
def get_user_restaurants(user_id):
    try:
        user_restaurants = services.get_user_restaurants(user_id)
        return jsonify(user_restaurants), 200
    except Exception as e:
        return jsonify(str(e)), 400
    
@main.route('/users/<int:user_id>/restaurants', methods=["POST"])
def post_user_restaurant(user_id):
    try:
        data = request.get_json()
        services.add_user_restaurant(user_id, data)
        return jsonify(f"Successfully added restaurant rating"), 200
    except Exception as e:
        return jsonify(str(e)), 400
    
@main.route("/users/<int:user_id>/restaurants/<int:restaurant_id>", methods=["DELETE"])
def del_user_restaurant(user_id, restaurant_id):
    try:
        services.delete_user_restaurant(user_id, restaurant_id)
        return jsonify(f"Successfully deleted rating for user_id: {user_id} and restaurant_id: {restaurant_id}"), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        return jsonify(str(e)), 400
    
@main.route("/users/<int:user_id>/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_user_restaurant(user_id, restaurant_id):
    try:
        data = request.get_json()
        services.update_user_restaurant(user_id, restaurant_id, data)
        return jsonify(f"Successfully updated rating for user_id: {user_id} and restaurant_id: {restaurant_id}"), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        return jsonify(str(e)), 400