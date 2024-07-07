from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Restaurant(db.Model):
    __tablename__ = 'RESTAURANT'
    __table_args__ = {'schema': 'RESTAURANT'}
    ID = db.Column(db.Integer, primary_key=True)
    YELP_BUSINESS_ID = db.Column(db.String(150), nullable=False, unique=True)
    NAME = db.Column(db.String(150), nullable=False, unique=False)
    ADDRESS = db.Column(db.String(150), nullable=True, unique=False)
    PHONE_NUMBER = db.Column(db.String(12), nullable=True, unique=True)
    MENU_ID = db.Column(db.Integer, db.ForeignKey("RESTAURANT.MENU.ID"), nullable=True, unique=True)
    MENU = db.relationship("MENU", backref="RESTAURANT")
    CATEGORIES = db.Column(ARRAY(db.String), nullable=True, unique=False)
    PRICE = db.Column(db.String(5), nullable=True, unique=False)
    RATING = db.Column(db.Float, nullable=True, unique=False)
    BUSINESS_HOURS_ID = db.Column(db.Integer, db.ForeignKey("RESTAURANT.BUSINESS_HOURS.ID"), nullable=True, unique=False)
    BUSINESS_HOURS = db.relationship("BUSINESS_HOURS", backref="RESTAURANT")
    CREATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    UPDATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Restaurant {self.title}>'
    
class BusinessHours(db.Model):
    __tablename__ = 'BUSINESS_HOURS'
    __table_args__ = {'schema': 'RESTAURANT'}
    ID = db.Column(db.Integer, primary_key=True)
    RESTAURANT_ID = db.Column(db.Integer, db.ForeignKey("RESTAURANT.RESTAURANT.ID"), nullable=False, unique=True)
    MONDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    TUESDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    WEDNESDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    THURSDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    FRIDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    SATURDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    SUNDAY = db.Column(ARRAY(db.Text), nullable=False, unique=False)
    CREATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    UPDATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Business Hours {self.ID}>'
    
class Menu(db.Model):
    __tablename__ = 'MENU'
    __table_args__ = {'schema': 'RESTAURANT'}
    ID = db.Column(db.Integer, primary_key=True)
    RESTAURANT_ID = db.Column(db.Integer, db.ForeignKey("RESTAURANT.RESTAURANT.ID"), nullable=False, unique=True)
    MENU_URL = db.Column(db.String(150), nullable=False, unique=True)
    POPULAR_DISHES = db.Column(db.String(150), nullable=False, unique=False)
    CREATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    UPDATED_AT = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<Menu {self.ID}>'