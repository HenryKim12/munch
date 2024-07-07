import requests
import os
from dotenv import load_dotenv

load_dotenv()

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

    # daysOfWeek = {
    #     0: "Monday",
    #     1: "Tuesday",
    #     2: "Wednesday",
    #     3: "Thursday",
    #     4: "Friday",
    #     5: "Saturday",
    #     6: "Sunday"
    # }

    response = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
    restaurants = response.json()["businesses"]
    for restaurant in restaurants:

        name = restaurant["name"]
        yelp_business_id = restaurant["id"]
        display_address = restaurant["location"]["display_address"]
        location = ""
        for address in display_address:
            location += address
        categoriesList = restaurant["categories"]
        categories =[]
        for category in categoriesList:
            categories.append(category["title"])
        priceRange = restaurant["price"]
        rating = restaurant["rating"]
        weeklyHours = restaurant["business_hours"]["open"]
        businessHours = []
        for i in range(7):
            day = ""
            dailyHours = weeklyHours[i]
            # businessHours += daysOfWeek[dailyHours["day"]]
            day += dailyHours["start"]
            day += " to "
            day += dailyHours["end"]
            businessHours.append(day)

        url = restaurant["url"]

    return response.json()
        

        

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