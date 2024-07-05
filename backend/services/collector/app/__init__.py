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
            "term": "restaurants",
            "limit": 50,
        }

        daysOfWeek = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
        restaurants = res["businesses"]
        for restaurant in restaurants:
            name = restaurant["name"]
            yelp_business_id = restaurant["id"]
            display_address = restaurant["location"]["display_address"]
            location = ""
            for address in display_address:
                location += address
            cuisine = restaurant["id"] #categories??
            priceRange = restaurant["price"]
            rating = restaurant["rating"]
            weeklyHours = restaurant["business_hours"]["open"]
            businessHours = ""
            for i in range(7):
                dailyHours = weeklyHours[i]
                businessHours += daysOfWeek[dailyHours["day"]]
                businessHours += " from "
                businessHours += dailyHours["start"]
                businessHours += " to "
                businessHours += dailyHours["end"]

        # Iterate through all of Vancouver restaurants
        # params = {
        #     "location": "Vancouver",
        #     "term": "restaurants",
        #     "limit": 50,
        #     "offset": 1
        # }
        # total = None
        # params["offset"] += 50
        # while (not total or params["offset"] <= total):
        #     res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
        #     params["offset"] += 50
        #     if not total:
        #         total = res.json()["total"]

        return "Successfully fetched Vancouver restaurants"

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