from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY
import os 
from dotenv import load_dotenv

load_dotenv()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yelp_business_id = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False, unique=False)
    address = db.Column(db.String(150), nullable=False, unique=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    menu = db.relationship('Menu', backref='restaurant', uselist=False, cascade="all, delete-orphan")
    categories = db.Column(ARRAY(db.String), nullable=False, unique=False)
    price = db.Column(db.String(5), nullable=False, unique=False)
    rating = db.Column(db.Float, nullable=False, unique=False)
    business_hours = db.relationship('BusinessHours', backref='restaurant', uselist=False, cascade="all, delete-orphan")
    yelp_url = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
class BusinessHours(db.Model):
    __tablename__ = 'business_hours'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(f'{os.getenv("SCHEMA")}.restaurant.id'), nullable=False, unique=True)
    monday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    tuesday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    wednesday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    thursday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    friday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    saturday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    sunday = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Business Hours {self.ID}>'
    
class Menu(db.Model):
    __tablename__ = 'menu'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(f'{os.getenv("SCHEMA")}.restaurant.id'), nullable=False, unique=True)
    url = db.Column(db.String(150), nullable=False, unique=True)
    popular_dishes = db.Column(ARRAY(db.String(150)), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Menu {self.ID}>'
