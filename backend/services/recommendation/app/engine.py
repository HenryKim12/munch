import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# content-based filtering
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

# collaborative filtering
from surprise import Dataset, Reader, SVD, accuracy
# from surprise.model_selection import train_test_split

load_dotenv()

def get_user_ratings(user_id):
    response = requests.get(f"{os.getenv("USER_API_URL")}/users/{user_id}/restaurants")
    return response.json()

def get_user_rated_restaurants(user_id):
    response = requests.get(f"{os.getenv("COLLECTOR_API_URL")}/restaurants/{user_id}/rated")
    return response.json()

def get_user_unrated_restaurants(user_id):
    response = requests.get(f"{os.getenv("COLLECTOR_API_URL")}/restaurants/{user_id}/unrated")
    return response.json()

def content_based_filtering(user_id):
    # [bar, outdoor seating, happy hour, vegan, pricing, rating]
    user_ratings = get_user_ratings(user_id)

    user_rated_restaurants = get_user_rated_restaurants(user_id)
    user_rated_restaurants_df = pd.json_normalize(user_rated_restaurants)
    
    train_data, test_data = train_test_split(user_rated_restaurants_df, test_size=0.2, random_state=42)

    user_unrated_restaurants = get_user_unrated_restaurants(user_id)
    user_unrated_restaurants_df = pd.json_normalize(user_unrated_restaurants)
    # add test_data to unrated restaurants to test accuracy 
    user_unrated_restaurants_df = pd.concat([user_unrated_restaurants_df, test_data], ignore_index=True)

    restaurantId_to_rating_map = {rating["restaurant_id"]: rating["rating"] for rating in user_ratings}
    recommendation_content = pd.DataFrame([row for i, row in train_data.iterrows() if restaurantId_to_rating_map[row["id"]] >= 4])
    recommendation_content_user_ratings = {}
    idx = 0
    for i, row in recommendation_content.iterrows():
        if restaurantId_to_rating_map[row["id"]] >= 4:
            recommendation_content_user_ratings[idx] = restaurantId_to_rating_map[row["id"]]
            idx += 1

    rated_feature_vectors = get_feature_vectors(recommendation_content)
    unrated_feature_vectors = get_feature_vectors(user_unrated_restaurants_df)
    feature_vectors = rated_feature_vectors + unrated_feature_vectors
    
    binary_features = [features[:4] for features in feature_vectors] # [bar, outdoor seating, happy hour, vegan]
    categorical_features = [features[4] for features in feature_vectors] # [price]
    numerical_features = [features[5] for features in feature_vectors] # [rating]

    encoder = OneHotEncoder(sparse_output=False)
    categorical_encoded = encoder.fit_transform(np.array(categorical_features).reshape(-1, 1))

    scaler = StandardScaler()
    numerical_standardized = pd.DataFrame(scaler.fit_transform(np.array(numerical_features).reshape(-1, 1)))

    feature_matrix = np.hstack([binary_features, categorical_encoded, numerical_standardized])
    similarity_matrix = cosine_similarity(feature_matrix)

    # aggregate similarity for unrated restaurant and weight it with the user ratings
    recommendation_scores = []
    for c in range(len(rated_feature_vectors), len(similarity_matrix[0])):
        score = 0
        for r in range(len(rated_feature_vectors)):
            score += similarity_matrix[r, c] * recommendation_content_user_ratings[r]
        recommendation_scores.append(score)

    restaurant_recommendation_map = {}
    for i in range(len(recommendation_scores)):
        restaurant_recommendation_map[user_unrated_restaurants_df.loc[i, "id"]] = recommendation_scores[i]

    sorted_restaurant_recommendation_mapping = sorted(restaurant_recommendation_map.items(), key=lambda x: x[1], reverse=True)

    N = 10
    top_recommendations = [id for id, score in sorted_restaurant_recommendation_mapping[:N]]
    return top_recommendations

def get_feature_vectors(df):
    feature_list = []
    for i, row in df.iterrows():
        features = [0] * 6
        for category in row["categories"]:
            if "bar" in category:
                features[0] = 1
            if "outdoor" in category:
                features[1] = 1
            if "happy hour" in category:
                features[2] = 1
            if "vegan" in category:
                features[3] = 1
        features[4] = row["price"]
        features[5] = row["rating"]
        feature_list.append(features)
    return feature_list 

def collaborative_filtering():
    # TODO: implement when data is less sparse (future feature)
    pass

