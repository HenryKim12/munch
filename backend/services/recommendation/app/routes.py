from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from app import engine

import os

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/users', methods=["GET"])
def get():
    try:
        
        return jsonify(), 200
    except Exception as e:
        print(str(e))
        return jsonify(str(e)), 400