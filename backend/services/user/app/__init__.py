from flask import Flask
from config import Config
from app.extensions import db
from dotenv import load_dotenv
from . import routes
from flask_migrate import Migrate
from flask_cors import CORS

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