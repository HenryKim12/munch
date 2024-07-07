import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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

    # response = requests.get(YELP_API_URL, headers=headers, params=params)
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
    #     # categories (people also searched for section) + popular dishes grabbed from scraping page

    # return response.json()
    return scrape("hi")

def scrape(url: str) -> list[str]: 
    response = requests.get("https://www.yelp.com/biz/the-flying-pig-vancouver-5?adjust_creative=SuhzlSss_Ymp7bpjhwEWSA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=SuhzlSss_Ymp7bpjhwEWSA")
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find_all("main", {"id": "main-content"})[0]
    section = main.find_all("section", {"aria-label": "People also searched for"})[0]
    categories = section.find_all("a")

    result = []
    for category in categories:
        value = category.find_all("p")[0]
        result.append(value.decode_contents())

    return result
        