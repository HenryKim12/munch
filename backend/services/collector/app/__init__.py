from flask import Flask
from config import Config
from app.extensions import db
from dotenv import load_dotenv
from .main import main as main_bp
import os
load_dotenv()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)

    return app