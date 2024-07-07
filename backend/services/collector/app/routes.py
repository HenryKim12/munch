from flask import Blueprint, render_template
from app.extensions import db
import requests
import os
from dotenv import load_dotenv
from . import services, models

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, this is the main index page."

@main.route('/about')
def about():
    return "This is the about page."

@main.route("/collect")
def collect():
    return services.fetchRestaurants()
    # return "Successfully fetched Vancouver restaurants"

# @main.route("/add_restaurant")
# def createRestaurant():
#     newRestaurant = models.Restaurant(id=1, title="McDonalds")
#     db.session.add(newRestaurant)
#     db.session.commit()
#     return 'User created successfully!'