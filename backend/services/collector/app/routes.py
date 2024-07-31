from flask import Blueprint, request, jsonify
from app.extensions import db
import requests
import os
from dotenv import load_dotenv
from . import services, models

load_dotenv()

main = Blueprint('main', __name__)

@main.route("/collect", methods=["GET"])
def collect():
    try:
        services.data_pipeline("Vancouver")
        return jsonify("Successfully fetched and updated restaurant data")
    except Exception as e:
        return jsonify(str(e))

@main.route('/restaurants', methods=["GET"])
def get():
    try:
        restaurants = services.get_restaurants()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/restaurants/<int:id>', methods=["GET"])
def getByID(id):
    try:
        restaurant = services.get_restaurant_by_id(id)
        return jsonify(restaurant), 200
    except ValueError as e:
        return jsonify(str(e)), 404
    except Exception as e:
        return jsonify(str(e)), 400
    
@main.route('/restaurants/<int:user_id>/unrated', methods=["GET"])
def get_unrated_restaurants(user_id):
    try:
        # data = request.get_json()
        unratedRestaurants = services.get_unrated_restaurants(user_id)
        return jsonify(unratedRestaurants), 200
    except Exception as e:
        return jsonify(str(e)), 400
    

@main.route('/restaurants/<int:user_id>/rated', methods=["GET"])
def get_rated_restaurants(user_id):
    try:
        unratedRestaurants = services.get_rated_restaurants(user_id)
        return jsonify(unratedRestaurants), 200
    except Exception as e:
        return jsonify(str(e)), 400