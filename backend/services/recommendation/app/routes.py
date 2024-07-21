from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from app import engine

import os

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/recommend/<int:user_id>', methods=["GET"])
def get(user_id):
    try:
        recommendation = engine.recommend(user_id)
        return jsonify(), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400