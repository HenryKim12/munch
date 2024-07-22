import requests
import os
import sys
import json
import traceback
import shutil
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from . import models
from app.extensions import db

load_dotenv()

YELP_API_URL = "https://api.yelp.com/v3/businesses/search"
OFFSET_LIMIT = 1000

def data_pipeline(location):
    try:
        restaurant_api_contents = fetch_yelp_api(location)
        print(f"[{datetime.now()}] Completed Yelp API fetch")

        restaurant_contents = scrape_restaurants(restaurant_api_contents)
        print(f"[{datetime.now()}] Completed scraping all Yelp pages")

        # with open('cache/prev_data.json', 'r') as json_file:
        #     restaurant_contents = json.load(json_file)

        update_db(restaurant_contents)
        print(f"[{datetime.now()}] Completed upsert into db")

        cache_data(restaurant_contents)
    except Exception as e:
        print(f"[{datetime.now()}] {str(e)}")
        raise Exception(f"[{datetime.now()}] {str(e)}")

def fetch_yelp_api(location):
    headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
    }
    params = {
        "location": location,
        "term": "restaurants",
        "limit": 50,
        "offset": 0
    }
    try:
        restaurant_api_contents = []
        total = None
        while (not total or (params["offset"] <= OFFSET_LIMIT and params["offset"] < total)):
            response = requests.get(YELP_API_URL, headers=headers, params=params)
            if not total:
                total = response.json()["total"]
            
            restaurants = response.json()["businesses"]
            count = 1
            for restaurant in restaurants:
                print(count)
                restaurant_valid = validate_api_result(restaurant)
                if not restaurant_valid:
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

                is_valid = validate_content(content)
                if not is_valid:
                    continue

                restaurant_api_contents.append(content)
                count += 1
            params["offset"] += 50
        return restaurant_api_contents
    except KeyError as e:
        raise Exception(f"Error while parsing yelp response: {str(e)}")
    except Exception as e:
        raise Exception(f"Error while fetching yelp api: {str(e)}")
    
def validate_api_result(restaurant) -> bool:
    return ("url" in restaurant and 
            "rating" in restaurant and 
            "price" in restaurant and 
            "business_hours" in restaurant and 
            "attributes" in restaurant and
            "business_hours" in restaurant and
            len(restaurant["business_hours"]) > 0 and
            "open" in restaurant["business_hours"][0])

def validate_content(content):
    is_valid = True
    for value in content.values():
        if not value:
            is_valid = False
            break
    return is_valid

def scrape_restaurants(restaurant_contents):
    for content in restaurant_contents:
        content["scraped_data"] = scrape(content["yelp_url"]) 

    new_restaurant_contents = []
    for i in range(len(restaurant_contents)):
        if restaurant_contents[i]["scraped_data"]:
            new_restaurant_contents.append(restaurant_contents[i])

    return new_restaurant_contents

def scrape(url: str) -> dict: 
    try:
        data = {}
        # "https://www.yelp.com/biz/the-flying-pig-vancouver-5?adjust_creative=SuhzlSss_Ymp7bpjhwEWSA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=SuhzlSss_Ymp7bpjhwEWSA"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, "html.parser")
        main_list = soup.find_all("main", id="main-content")
        if len(main_list) == 0:
            return {}
        main = main_list[0]

        menu_section_list = main.find_all("section", attrs={"class": "y-css-rgh890", "aria-label": "Menu"})
        if len(menu_section_list) == 0:
            return {}
        menu_section = menu_section_list[0]
        dish_result = []
        dish_tags = menu_section.find_all("p", attrs={"class": "y-css-tnxl0n", "data-font-weight": "bold"})
        if len(dish_tags) == 0:
            return {}
        for dish_tag in dish_tags:
            dish = dish_tag.decode_contents()
            dish_result.append(dish)
        data["menu"] = dish_result

        categories_section_list = main.find_all("section", attrs={"class": "y-css-rgh890", "aria-label": "People also searched for"})
        if len(categories_section_list) == 0:
            return {}
        categories_section = categories_section_list[0]

        categories_result = []
        category_tags = categories_section.find_all("p", attrs={"class": "y-css-1o34y7f", "data-font-weight": "semibold"})
        if len(category_tags) == 0:
            return {}
        for category_tag in category_tags:
            category = category_tag.decode_contents()
            categories_result.append(category)
        data["categories"] = categories_result
        return data
    except Exception as e:    
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)     
        raise Exception(f"Error while scraping yelp restaurant url: {str(e)}")

def update_db(restaurant_contents: list[dict]) -> None:
    try:
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
                monday=content["business_hours"]["0"], 
                tuesday=content["business_hours"]["1"], 
                wednesday=content["business_hours"]["2"], 
                thursday=content["business_hours"]["3"], 
                friday=content["business_hours"]["4"], 
                saturday=content["business_hours"]["5"], 
                sunday=content["business_hours"]["6"], 
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
    except Exception as e:
        print(traceback.print_exc())
        raise Exception(f"Error while update database with restaurant data: {str(e)}")

def restaurant_exists(yelp_business_id: str) -> bool:
    return db.session.query(db.exists().where(models.Restaurant.yelp_business_id == yelp_business_id)).scalar()

def update_restaurant(content: dict) -> None:
    restaurant = models.Restaurant.query.filter_by(yelp_business_id=content["yelp_business_id"]).first()

    # TODO: use cached values to compare instead of using db operation?? also use in get, getbyID??
    # with open('cache/prev_data.json', 'r') as json_file:
    #         restaurant_contents = json.load(json_file)

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
    if restaurant.business_hours.monday != content["business_hours"]["0"]: 
        restaurant.business_hours.monday = content["business_hours"]["0"]
        business_hours_updated = True
    if restaurant.business_hours.tuesday != content["business_hours"]["1"]: 
        restaurant.business_hours.tuesday = content["business_hours"]["1"]
        business_hours_updated = True
    if restaurant.business_hours.wednesday != content["business_hours"]["2"]: 
        restaurant.business_hours.wednesday = content["business_hours"]["2"]
        business_hours_updated = True
    if restaurant.business_hours.thursday != content["business_hours"]["3"]: 
        restaurant.business_hours.thursday = content["business_hours"]["3"]
        business_hours_updated = True
    if restaurant.business_hours.friday != content["business_hours"]["4"]: 
        restaurant.business_hours.friday = content["business_hours"]["4"]
        business_hours_updated = True
    if restaurant.business_hours.saturday != content["business_hours"]["5"]: 
        restaurant.business_hours.saturday = content["business_hours"]["5"]
        business_hours_updated = True
    if restaurant.business_hours.sunday != content["business_hours"]["6"]: 
        restaurant.business_hours.sunday = content["business_hours"]["6"]
        business_hours_updated = True
    if business_hours_updated:
        restaurant.business_hours.updated_at = db.func.current_timestamp()

    db.session.commit()

def cache_data(restaurant_contents):
    if os.path.exists('cache/prev_data.json'):
        shutil.move('cache/prev_data.json', f"cache/old/{datetime.now().strftime('%Y_%m_%d %H:%M:%S')}.json")
    
    with open('cache/prev_data.json', 'w') as json_file:
        json.dump(restaurant_contents, json_file, indent=4)
    print("Cached newly upserted data")

def get_restaurants():
    restaurants = models.Restaurant.query.all()
    return restaurants

def get_restaurant_by_id(id):
    restaurant = db.session.get(models.Restaurant, id)
    if not restaurant:
        raise ValueError("Restaurant does not exist.")
    return restaurant

def get_unrated_restaurants(user_id, data):
    rated_ids = data["rated_restaurants"]
    