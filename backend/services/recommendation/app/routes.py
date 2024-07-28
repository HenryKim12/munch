from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from app import engine

import os

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/recommend/content/<int:user_id>', methods=["GET"])
def get_content_based_recommendation(user_id):
    try:
        recommendations = engine.content_based_filtering(user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400
    
@main.route('/recommend/collab', methods=["GET"])
def get_collaborative_recommendation():
    try:
        recommendations = engine.collaborative_filtering()
        return jsonify(recommendations), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400
    
