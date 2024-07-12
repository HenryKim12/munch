from flask import Blueprint, render_template
from app.extensions import db
import requests
import os
from dotenv import load_dotenv
from . import services, models

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/restaurants', methods=["GET"])
def get():
    return services.get_restaurants()

@main.route('/restaurants/<int:id>', methods=["GET"])
def getByID(id):
    return services.get_restaurant_by_id(id)

@main.route("/collect", methods=["GET"])
def collect():
    try:
        services.fetchRestaurants()
        return "Success"
    except Exception as error:
        return str(error)