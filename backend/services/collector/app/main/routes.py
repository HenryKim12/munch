from flask import render_template
from . import main
from app.extensions import db
from ..models import Restaurant
import requests
import os
from dotenv import load_dotenv
from . import services

load_dotenv()

@main.route('/')
def index():
    return "Hello, this is the main index page."

@main.route('/about')
def about():
    return "This is the about page."

@main.route("/collect")
def collect():
    services.fetchRestaurants()
    return "Successfully fetched Vancouver restaurants"

@main.route("/add_restaurant")
def createRestaurant():
    newRestaurant = Restaurant(id=1, title="McDonalds")
    db.session.add(newRestaurant)
    db.session.commit()
    return 'User created successfully!'