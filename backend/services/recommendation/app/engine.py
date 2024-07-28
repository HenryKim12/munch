import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# content-based filtering
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# collaborative filtering
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split


load_dotenv()

def get_user_ratings(user_id):
    response = requests.get(f"{os.getenv("USER_API_URL")}/users/{user_id}/restaurants")
    return response.json()

def get_user_rated_restaurants(user_ratings):
    restaurant_ids = [user_rating["restaurant_id"] for user_rating in user_ratings]
    response = requests.post(f"{os.getenv("RESTAURANT_API_URL")}/restaurants/rated", json={"restaurant_ids": restaurant_ids})
    return response.json()

def get_user_unrated_restaurants(user_ratings):
    rated_restaurant_ids = [rating["restaurant_id"] for rating in user_ratings]
    response = requests.post(f"{os.getenv("RESTAURANT_API_URL")}/restaurants/unrated", json={"rated_restaurants": rated_restaurant_ids})
    return response.json()

def content_based_filtering(user_id):
    # [bar/happy hour, outdoor seating, parking, vegan, pricing, rating]
    user_ratings = get_user_ratings(user_id)

    user_rated_restaurants = get_user_rated_restaurants(user_ratings)
    user_restaurant_ratings_df = pd.json_normalize(user_rated_restaurants)
    user_restaurant_ratings_df.sort_values(by=["rating"], ascending=False)

    user_unrated_restaurants = get_user_unrated_restaurants(user_ratings)
    user_unrated_restaurants_df = pd.json_normalize(user_unrated_restaurants)

    content_limit = 5
    if user_restaurant_ratings_df.shape[0] < 5:
        content_limit = user_restaurant_ratings_df.shape[0]

    rated_features_list = []
    for i, row in user_restaurant_ratings_df.iterrows():
        if i == content_limit:
            break

        rated_features = [0] * 6
        for category in row["categories"]:
            if "bar" in category or "happy hour" in category:
                rated_features[0] = 1
            if "outdoor" in category:
                rated_features[1] = 1
            if "parking" in category:
                rated_features[2] = 1
            if "vegan" in category:
                rated_features[3] = 1
        rated_features[4] = row["price"]
        rated_features[5] = row["rating"]
        rated_features_list.append(rated_features) 

    unrated_features_list = []
    for i, row in user_unrated_restaurants_df.iterrows():
        unrated_features = [0] * 6
        for category in row["categories"]:
            if "bar" in category or "happy hour" in category:
                unrated_features[0] = 1
            if "outdoor" in category:
                unrated_features[1] = 1
            if "parking" in category:
                unrated_features[2] = 1
            if "vegan" in category:
                unrated_features[3] = 1
        unrated_features[4] = row["price"]
        unrated_features[5] = row["rating"]
        unrated_features_list.append(unrated_features) 

    # first content_limit rows (< 5) are rated features, rest are unrated features we want to predict
    features_matrix = []
    features_matrix.extend(rated_features_list)
    features_matrix.extend(unrated_features_list)
    
    binary_features = [features[:4] for features in features_matrix] # [bar/happy hour, outdoor seating, parking, vegan]
    categorical_features = [features[4] for features in features_matrix] # [price]
    numerical_features = [features[5] for features in features_matrix] # [rating]

    encoder = OneHotEncoder(sparse_output=False)
    categorical_encoded = encoder.fit_transform(np.array(categorical_features).reshape(-1, 1))

    scaler = StandardScaler()
    numerical_standardized = pd.DataFrame(scaler.fit_transform(np.array(numerical_features).reshape(-1, 1)))

    feature_vectors = np.hstack([binary_features, categorical_encoded, numerical_standardized])
    similarity_matrix = cosine_similarity(feature_vectors)

    recommendation_scores = []
    for c in range(content_limit, len(similarity_matrix[0])):
        score = 0
        for r in range(content_limit):
            score += similarity_matrix[r, c] * user_ratings[r]["rating"]
        recommendation_scores.append(score)

    restaurant_recommendation_mapping = {}
    for i in range(len(user_unrated_restaurants)):
        restaurant_recommendation_mapping[user_unrated_restaurants[i]["id"]] = recommendation_scores[i]

    sorted_restaurant_recommendation_mapping = sorted(restaurant_recommendation_mapping.items(), key=lambda x: x[1], reverse=True)

    N = 10
    top_recommendations = [id for id, score in sorted_restaurant_recommendation_mapping[:N]]
    return top_recommendations

def collaborative_filtering():
    pass
#     user_restaurant_ratings = get_user_ratings(user_id)
#     rated_data = pd.json_normalize(user_restaurant_ratings)

#     user_unrated_restaurant_ids = get_unrated_restaurant_ids(user_restaurant_ratings)

#     reader = Reader(rating_scale=(0, 5))
#     surprise_data = Dataset.load_from_df(rated_data[['user_id', 'restaurant_id', 'rating']], reader)
#     trainset, testset = train_test_split(surprise_data, test_size=0.25)

#     algo = SVD()
#     algo.fit(trainset)
#     test_prediction = algo.test(testset)
#     accuracy.rmse(test_prediction)

#     predictions = [algo.predict(user_id, unrated_restaurant) for unrated_restaurant in user_unrated_restaurant_ids]
#     return predictions
