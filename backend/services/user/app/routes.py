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

@main.route('/users/<int:id>', methods=["DELETE"])
def delete(id):
    pass

@main.route('/users', methods=["POST"])
def post():
    pass

@main.route('/users', methods=["PUT"])
def update():
    pass