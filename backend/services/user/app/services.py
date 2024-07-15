import os
from dotenv import load_dotenv
from . import models
from flask import jsonify
from .extensions import db
import bcrypt

load_dotenv()

def get_users():
    users = models.User.query.all()
    return jsonify(users)

def get_user_by_id(id):
    user = models.User.get(id)
    return jsonify(user)

def delete_user(id):
    user = models.User.get(id)
    db.session.delete(user)
    db.session.commit()

def create_user(data):
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
    user = models.User.get(id)
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