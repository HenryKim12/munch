from flask import Blueprint, request, jsonify
from app.extensions import db
import requests
import os
from dotenv import load_dotenv
from . import services, models

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/restaurants', methods=["GET"])
def get():
    try:
        restaurants = services.get_restaurants()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route('/restaurants/<int:id>', methods=["GET"])
def getByID():
    try:
        restaurant = services.get_restaurant_by_id(request.args.get("id"))
        return jsonify(restaurant), 200
    except Exception as e:
        return jsonify(str(e)), 400

@main.route("/collect", methods=["GET"])
def collect():
    try:
        services.fetchRestaurants()
        return jsonify("Successfully fetched and updated restaurant data")
    except Exception as e:
        return jsonify(str(e))