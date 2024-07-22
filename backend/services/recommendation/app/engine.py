import requests
import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

def get_user_ratings(user_id):
    response = requests.get(f"http://127.0.0.1:5002/users/{user_id}/restaurants")
    return response.json()

def get_unrated_restaurants(user_id, user_ratings):
    rated_restaurant_ids = [rating.restaurant_id for rating in user_ratings]
    
    pass

def recommend(user_id):
    user_ratings = get_user_ratings(user_id)
    data = pd.json_normalize(user_ratings)
    reader = Reader(rating_scale=(1, 5))
    surprise_data = Dataset.load_from_df(data[['user_id', 'restaurant_id', 'rating']], reader)
    trainset, testset = train_test_split(surprise_data, test_size=0.25)

    algo = SVD()
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions)
    return "hi"