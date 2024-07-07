from flask import Flask
from config import Config
from app.extensions import db
from dotenv import load_dotenv
from . import routes

import os
load_dotenv()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        app.register_blueprint(routes.main)
        db.create_all()

    return app