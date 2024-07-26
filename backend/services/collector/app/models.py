from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY
import os 
from dotenv import load_dotenv

load_dotenv()

# flask db init (only once at beginning)
# flask db migrate -m "message"
# flask db upgrade

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yelp_business_id = db.Column(db.String(150), nullable=False, unique=True)
    name = db.Column(db.String(150), nullable=False, unique=False)
    address = db.Column(db.String(150), nullable=False, unique=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=False)
    menu = db.relationship('Menu', backref='restaurant', uselist=False, cascade="all, delete-orphan", single_parent=True)
    categories = db.Column(ARRAY(db.String), nullable=False, unique=False)
    price = db.Column(db.String(5), nullable=False, unique=False)
    rating = db.Column(db.Float, nullable=False, unique=False)
    business_hours = db.relationship('BusinessHours', backref='restaurant', uselist=False, cascade="all, delete-orphan", single_parent=True)
    yelp_url = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "yelp_business_id": self.yelp_business_id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "menu": self.menu.to_dict(),
            "categories": self.categories,
            "price": self.price,
            "rating": self.rating,
            "business_hours": self.business_hours.to_dict(),
            "yelp_url": self.yelp_url,
        }
    
class BusinessHours(db.Model):
    __tablename__ = 'business_hours'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(f'{os.getenv("SCHEMA")}.restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    monday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    tuesday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    wednesday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    thursday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    friday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    saturday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    sunday = db.Column(ARRAY(db.Text), nullable=True, unique=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Business Hours {self.ID}>'

    def to_dict(self):
        return {
            "id": self.id,
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "saturday": self.saturday,
            "sunday": self.sunday,
        }
    
class Menu(db.Model):
    __tablename__ = 'menu'
    __table_args__ = {'schema': os.getenv("SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(f'{os.getenv("SCHEMA")}.restaurant.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, unique=True)
    url = db.Column(db.String(150), nullable=False, unique=False)
    popular_dishes = db.Column(ARRAY(db.String(150)), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Menu {self.ID}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "popular_dishes": self.popular_dishes
        }
