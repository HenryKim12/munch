from app.extensions import db

class Restaurant(db.Model):
    __table_args__ = {'schema': 'restaurant'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    yelp_business_id = db.Column(db.String(150))
    location = db.Column(db.String(150))
    cuisine = db.Column(db.String(150))
    price_range = db.Column(db.String(150))
    rating = db.Column(db.Float)
    business_hours = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Restaurant {self.title}>'