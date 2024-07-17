from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from app.extensions import db
from app import routes

import os

load_dotenv()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db, include_schemas=True)
    with app.app_context():
        app.register_blueprint(routes.main)

    return app