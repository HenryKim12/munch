import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from . import models
from app.extensions import db

load_dotenv()

YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

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
def fetchRestaurants():
    headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
    }
    try:
        params = {
            "location": "Vancouver",
            "term": "restaurants",
            "limit": 3,
        }
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        restaurants = response.json()["businesses"]
        for restaurant in restaurants:
            yelp_business_id = restaurant["id"]
            name = restaurant["name"]
            phone_number = restaurant["display_phone"]
            menu_url = restaurant["attributes"]["menu_url"]
            price = restaurant["price"]
            rating = restaurant["rating"]

            address = ""
            display_address = restaurant["location"]["display_address"]
            for val in display_address:
                address += val

            open_hours = restaurant["business_hours"]["open"]
            business_hours = {k: [] for k in range(7)}
            for val in open_hours:
                daily_hours = f"{val["start"]}-{val["end"]}"
                business_hours[val["day"]].append(daily_hours)

            url = restaurant["url"]
            scraped_data = scrape(url) # categories (people also searched for section) + popular dishes grabbed from scraping page

            menu_instance = models.Menu(menu_url=menu_url, popular_dishes=scraped_data["menu"])
            db.session.add(menu_instance)

            businessHours_instance = models.BusinessHours(
                monday=business_hours[0], 
                tuesday=business_hours[1], 
                wednesday=business_hours[2], 
                thursday=business_hours[3], 
                friday=business_hours[4], 
                saturday=business_hours[5], 
                sunday=business_hours[6], 
            )
            db.session.add(businessHours_instance)

            restaurant_instance = models.Restaurant(
                yelp_business_id= yelp_business_id,
                name= yelp_business_id,
                address= yelp_business_id,
                phone_number= yelp_business_id,
                menu= menu_instance,
                categories= scraped_data["categories"],
                price= price,
                rating= rating,
                business_hours= businessHours_instance,
                yelp_url= url,
            )
            db.session.add(restaurant_instance)
            db.session.commit()

    except Exception as error:
        print(f"[{datetime.now()}] Error while collecting restaurant data: {error}")
        return "Fail"

    return "Success"

def scrape(url: str) -> dict: 
    try:
        data = {}
        response = requests.get("https://www.yelp.com/biz/the-flying-pig-vancouver-5?adjust_creative=SuhzlSss_Ymp7bpjhwEWSA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=SuhzlSss_Ymp7bpjhwEWSA")
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find_all("main", id="main-content")[0]

        menu_section = main.find_all("section", attrs={"class": "y-css-rgh890", "aria-label": "Menu"})
        dish_result = []
        dish_tags = menu_section.find_all("p", attrs={"class": "y-css-tnxl0n", "data-font-weight": "bold"})
        for dish_tag in dish_tags:
            dish = dish_tag.decode_contents()
            dish_result.append(dish)
        data["menu"] = dish_result

        categories_section = main.find_all("section", attrs={"class": "y-css-rgh890", "aria-label": "People also searched for"})[0]
        categories_result = []
        category_tags = categories_section.find_all("p", attrs={"class": "y-css-1o34y7f", "data-font-weight": "semibold"})
        for category_tag in category_tags:
            category = category_tag.decode_contents()
            categories_result.append(category)
        data["categories"] = categories_result

    except Exception as error: 
        print(f"[{datetime.now()}] Error while scraping yelp restaurant url: {error}")
        raise Exception(error)

    return data