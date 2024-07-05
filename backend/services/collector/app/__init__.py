from flask import Flask
from config import Config
from app.extensions import db
from .Restaurant import Restaurant
import requests
from dotenv import load_dotenv
import os
load_dotenv()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # fectching data from api
    @app.route("/fetch")
    def fetchRestaurants():
        headers = {
            "accept": "application/json", 
            "Authorization": f"Bearer {os.getenv("API_KEY")}",
        }
        params = {
            "location": "Vancouver",
            "term": "restaurants"
        }
        response = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
        print(response.json())
        return response.json()

    @app.route("/get")
    def getAllRestaurants():
        return ""
    
    # @app.route("/get/:id")
    # def getAllRestaurants():
    #     return ""

    @app.route("/add_restaurant")
    def createRestaurant():
        newRestaurant = Restaurant(id=1, title="McDonalds")
        db.session.add(newRestaurant)
        db.session.commit()
        return 'User created successfully!'

    return app