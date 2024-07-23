import os
import requests
import pandas as pd
from dotenv import load_dotenv
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

load_dotenv()

def get_user_ratings(user_id):
    response = requests.get(f"{os.getenv("USER_API_URL")}/users/{user_id}/restaurants")
    return response.json()

def get_unrated_restaurants(user_ratings):
    rated_restaurant_ids = [rating["restaurant_id"] for rating in user_ratings]
    response = requests.post(f"{os.getenv("RESTAURANT_API_URL")}/restaurants", json={"rated_restaurants": rated_restaurant_ids})
    return response.json()

def recommend(user_id):
    user_restaurant_ratings = get_user_ratings(user_id)
    rated_data = pd.json_normalize(user_restaurant_ratings)

    user_unrated_restaurants = get_unrated_restaurants(user_restaurant_ratings)

    reader = Reader(rating_scale=(0, 5))
    surprise_data = Dataset.load_from_df(rated_data[['user_id', 'restaurant_id', 'rating']], reader)
    trainset, testset = train_test_split(surprise_data, test_size=0.25)

    algo = SVD()
    algo.fit(trainset)
    test_prediction = algo.test(testset)
    accuracy.rmse(test_prediction)

    predictions = [algo.predict(user_id, unrated_restaurant) for unrated_restaurant in user_unrated_restaurants]
    return "hi"