from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY
from dotenv import load_dotenv

import os 

load_dotenv()

class User(db.Model):
    __tablename__ = 'usr'
    __table_args__ = {'schema': os.getenv("USER_SCHEMA"), 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    restaurants = db.relationship('UserRestaurant', back_populates='user', cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "restaurants": self.restaurants
        }

class UserRestaurant(db.Model):
    __tablename__ = 'user_restaurant'
    __table_args__ = {'schema': os.getenv("USER_SCHEMA"), 'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{os.getenv("USER_SCHEMA")}.usr.id'), nullable=False)  
    restaurant_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='restaurants')  