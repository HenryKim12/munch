from app.extensions import db
from sqlalchemy.dialects.postgresql import ARRAY
import os 
from dotenv import load_dotenv

load_dotenv()

# user_restaurant = db.Table('user_restaurant', 
#     db.Column('user_id', db.Integer, db.ForeignKey(f'{os.getenv("USER_SCHEMA")}.user.id')),
#     db.Column('restaurant_id', db.Integer, db.ForeignKey(f'{os.getenv("RESTAURANT_SCHEMA")}.restaurant.id'))
# )

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': os.getenv("USER_SCHEMA")}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # restaurants = db.relationship('Restaurant', secondary=user_restaurant, backref='users')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, unique=False)

    def __repr__(self):
        return f'<User {self.username}>'
    