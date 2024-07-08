import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

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
    params = {
        "location": "Vancouver",
        "term": "restaurants",
        "limit": 50,
    }

    response = requests.get(YELP_API_URL, headers=headers, params=params)
    # restaurants = response.json()["businesses"]
    # for restaurant in restaurants:
    #     yelp_business_id = restaurant["id"]
    #     name = restaurant["name"]
    #     phone_number = restaurant["display_phone"]
    #     menu_url = restaurant["attributes"]["menu_url"]
    #     price = restaurant["price"]
    #     rating = restaurant["rating"]

    #     address = ""
    #     display_address = restaurant["location"]["display_address"]
    #     for val in display_address:
    #         address += val

    #     open_hours = restaurant["business_hours"]["open"]
    #     business_hours = {k: [] for k in range(7)}
    #     for val in open_hours:
    #         daily_hours = f"{val["start"]} to {val["end"]}"
    #         business_hours[val["day"]].append(daily_hours)

    #     url = restaurant["url"]
    #     scraped_data = scrape(url)
    #     # categories (people also searched for section) + popular dishes grabbed from scraping page

    # return response.json()

    return scrape("hi")

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
        data["error"] = True
        print(f"[{datetime.now()}] Error while scraping yelp url: {error}")

    finally: 
        return data