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
def fetchRestaurants() -> None:
    headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
    }
    try:
        params = {
            "location": "Vancouver",
            "term": "restaurants",
            "limit": 1,
        }
        restaurant_contents = []
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        restaurants = response.json()["businesses"]
        for restaurant in restaurants:
            if not (restaurant["url"] and restaurant["rating"] and restaurant["price"] and restaurant["business_hours"] and 
                    restaurant["attributes"]):
                continue

            content = {}
            content["yelp_business_id"] = restaurant["id"]
            content["name"] = restaurant["name"]
            content["phone_number"] = restaurant["display_phone"]
            content["menu_url"] = restaurant["attributes"]["menu_url"]
            content["price"] = restaurant["price"]
            content["rating"] = restaurant["rating"]
            content["yelp_url"] = restaurant["url"]

            address = ""
            display_address = restaurant["location"]["display_address"]
            for val in display_address:
                address += val
            content["address"] = address

            open_hours = restaurant["business_hours"][0]["open"]
            business_hours = {k: [] for k in range(7)}
            for val in open_hours:
                daily_hours = f"{val["start"]} - {val["end"]}"
                business_hours[val["day"]].append(daily_hours)
            content["business_hours"] = business_hours

            is_valid = True
            for value in content.values():
                if not value:
                    is_valid = False
                    break
            if not is_valid:
                continue

            # categories (people also searched for section) + popular dishes grabbed from scraping page
            content["scraped_data"] = scrape(content["yelp_url"]) 
            restaurant_contents.append(content)

        update_db(restaurant_contents)
    except Exception as error:
        print(f"[{datetime.now()}] Error while collecting restaurant data: {error}")
        raise Exception(f"[{datetime.now()}] Error while collecting restaurant data: {error}")

def update_db(restaurant_contents: list[dict]) -> None:
    for content in restaurant_contents:
        exists = restaurant_exists(content["yelp_business_id"])
        if exists:
            update_restaurant(content)
            continue
            
        menu_instance = models.Menu(
                url=content["menu_url"], 
                popular_dishes=content["scraped_data"]["menu"]
            )
        db.session.add(menu_instance)

        businessHours_instance = models.BusinessHours(
            monday=content["business_hours"][0], 
            tuesday=content["business_hours"][1], 
            wednesday=content["business_hours"][2], 
            thursday=content["business_hours"][3], 
            friday=content["business_hours"][4], 
            saturday=content["business_hours"][5], 
            sunday=content["business_hours"][6], 
        )
        db.session.add(businessHours_instance)

        restaurant_instance = models.Restaurant(
            yelp_business_id= content["yelp_business_id"],
            name= content["name"],
            address= content["address"],
            phone_number= content["phone_number"],
            menu= menu_instance,
            categories= content["scraped_data"]["categories"],
            price= content["price"],
            rating= content["rating"],
            business_hours= businessHours_instance,
            yelp_url= content["yelp_url"],
        )
        db.session.add(restaurant_instance)
        db.session.commit()

def scrape(url: str) -> dict: 
    try:
        data = {}
        # "https://www.yelp.com/biz/the-flying-pig-vancouver-5?adjust_creative=SuhzlSss_Ymp7bpjhwEWSA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=SuhzlSss_Ymp7bpjhwEWSA"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find_all("main", id="main-content")[0]

        menu_section = main.find_all("section", attrs={"class": "y-css-rgh890", "aria-label": "Menu"})[0]
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
        raise Exception(f"[{datetime.now()}] Error while scraping yelp restaurant url: {error}")

    return data

def restaurant_exists(yelp_business_id: str) -> bool:
    return db.session.query(db.exists().where(models.Restaurant.yelp_business_id == yelp_business_id)).scalar()

def update_restaurant(content: dict) -> None:
    restaurant = models.Restaurant.query.filter_by(yelp_business_id=content["yelp_business_id"]).first()

    # update restaurants
    restaurant_updated = False
    if restaurant.name != content["name"]: 
        restaurant.name = content["name"]
        restaurant_updated = True
    if restaurant.address != content["address"]: 
        restaurant.address = content["address"]
        restaurant_updated = True
    if restaurant.phone_number != content["phone_number"]: 
        restaurant.phone_number = content["phone_number"]
        restaurant_updated = True
    if restaurant.price != content["price"]: 
        restaurant.price = content["price"]
        restaurant_updated = True
    if restaurant.rating != content["rating"]: 
        restaurant.rating = content["rating"]
        restaurant_updated = True
    if restaurant.yelp_url != content["yelp_url"]: 
        restaurant.yelp_url = content["yelp_url"]
        restaurant_updated = True
    for category in content["scraped_data"]["categories"]:
        if not (category in restaurant.categories):
            restaurant.categories.append(category)
            restaurant_updated = True
    if restaurant_updated:
        restaurant.updated_at = db.func.current_timestamp()

    # update menus
    menu_updated = False
    if restaurant.menu.url != content["menu_url"]: 
        restaurant.menu.url = content["menu_url"]
        menu_updated = True
    for dish in content["scraped_data"]["menu"]:
        if not (dish in restaurant.menu.popular_dishes):
            restaurant.menu.popular_dishes.append(dish)
            menu_updated = True
    if menu_updated:
        restaurant.menu.updated_at = db.func.current_timestamp()

    # update business_hours
    business_hours_updated = False
    if restaurant.business_hours.monday != content["business_hours"][0]: 
        restaurant.business_hours.monday = content["business_hours"][0]
        business_hours_updated = True
    if restaurant.business_hours.tuesday != content["business_hours"][1]: 
        restaurant.business_hours.tuesday = content["business_hours"][1]
        business_hours_updated = True
    if restaurant.business_hours.wednesday != content["business_hours"][2]: 
        restaurant.business_hours.wednesday = content["business_hours"][2]
        business_hours_updated = True
    if restaurant.business_hours.thursday != content["business_hours"][3]: 
        restaurant.business_hours.thursday = content["business_hours"][3]
        business_hours_updated = True
    if restaurant.business_hours.friday != content["business_hours"][4]: 
        restaurant.business_hours.friday = content["business_hours"][4]
        business_hours_updated = True
    if restaurant.business_hours.saturday != content["business_hours"][5]: 
        restaurant.business_hours.saturday = content["business_hours"][5]
        business_hours_updated = True
    if restaurant.business_hours.sunday != content["business_hours"][6]: 
        restaurant.business_hours.sunday = content["business_hours"][6]
        business_hours_updated = True
    if business_hours_updated:
        restaurant.business_hours.updated_at = db.func.current_timestamp()

    db.session.commit()

def get_restaurants():
    restaurants = models.Restaurant.query.all()
    return restaurants

def get_restaurant_by_id(id):
    restaurant = models.Restaurant.get(id)
    return restaurant