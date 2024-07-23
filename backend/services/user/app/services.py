from dotenv import load_dotenv
from app import models
from flask import jsonify
from app.extensions import db
from sqlalchemy import and_

import os
import bcrypt

load_dotenv()

def get_users():
    users = models.User.query.all()
    response = []
    for user in users:
        response.append(user.to_dict())
    return response

def get_user_by_id(id):
    user = db.session.get(models.User, id)
    if not user:
        raise ValueError("User does not exist.")
    return user.to_dict()

def delete_user(id):
    user = db.session.get(models.User, id)
    if not user:
        raise ValueError("User does not exist.")
    db.session.delete(user)
    db.session.commit()

def create_user(data):
    existingUsername = db.session.query(db.exists().where(models.User.username == data["username"])).scalar()
    existingEmail = db.session.query(db.exists().where(models.User.email == data["email"])).scalar()
    if existingUsername or existingEmail:
        raise ValueError("Account with given username/email already exists. Try signing in.")
    
    user = models.User(username= data["username"],
                       email= data["email"],
                       password= hash_password(data["password"]),
                       restaurants=[]              
    )
    db.session.add(user)
    db.session.commit()

def hash_password(password) -> str:
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt) 
    return hash

def update_user(id, data):
    user = db.session.get(models.User, id)
    if not user:
        raise ValueError("User does not exist.")
    
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = hash_password(data["password"])
    if "restaurants" in data:
        for restaurant in data["restaurants"]:
            user.restaurants.append(restaurant)
    db.session.commit()

def get_user_restaurants(user_id):
    user_restaurants = models.UserRestaurant.query.filter_by(user_id=user_id)
    res = []
    for user_restaurant in user_restaurants:
        res.append(user_restaurant.to_dict())
    return res

def add_user_restaurant(user_id, data):
    existingRating = db.session.query(models.UserRestaurant.id).filter(and_(models.UserRestaurant.user_id == user_id, 
                                                                            models.UserRestaurant.restaurant_id == data["restaurant_id"])).first()
    if existingRating:
        raise ValueError("Rating already exists for restaurant.")
    
    user_restaurant = models.UserRestaurant(
        user_id = user_id,
        restaurant_id=data["restaurant_id"],
        rating=data["rating"]
    )
    db.session.add(user_restaurant)
    db.session.commit()

def delete_user_restaurant(user_id, restaurant_id):
    existingRating = db.session.query(models.UserRestaurant.id).filter(and_(models.UserRestaurant.user_id == user_id, 
                                                                            models.UserRestaurant.restaurant_id == restaurant_id)).first()
    if not existingRating:
        raise ValueError("User does not have rating for restaurant")

    db.session.delete(existingRating)
    db.session.commit()

def update_user_restaurant(user_id, restaurant_id, data):
    existingRating = db.session.query(models.UserRestaurant.id).filter(and_(models.UserRestaurant.user_id == user_id, 
                                                                            models.UserRestaurant.restaurant_id == restaurant_id)).first()
    
    if not existingRating:
        raise ValueError("User does not have rating for restaurant")
    
    if "rating" in data:
        existingRating.rating = data["rating"]
    
    db.session.commit()

