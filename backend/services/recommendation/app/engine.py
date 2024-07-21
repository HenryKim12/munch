import requests
import pandas as pd
# from surprise import Dataset, Reader, SVD, accuracy
# from surprise.model_selection import train_test_split

def get_user_ratings(user_id):
    response = requests.get(f"http://127.0.0.1:5002/users/{user_id}/restaurants")
    return response.json()

def recommend(user_id):
    user_ratings = get_user_ratings(user_id)
    return user_ratings