from flask import Blueprint, render_template
from app.extensions import db
import os
from dotenv import load_dotenv
from . import models

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/users', methods=["GET"])
def get():
    pass
@main.route('/users/<int:id>', methods=["GET"])
def getByID(id):
    pass