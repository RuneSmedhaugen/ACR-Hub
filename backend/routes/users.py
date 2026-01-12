from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from bson import ObjectId

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    db_ = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    avatar = data.get('avatar', '')
    bio = data.get('bio', '')
    age = data.get('age', 0)
    car = data.get('car', '')
    location = data.get('location', '')
    team = data.get('team', '')


    if db_.users.find_one({'username': username}):
        return jsonify({"msg": "Username already exists"}), 400
    
    hashed_password = generate_password_hash(password)

    user_doc = {
        'username': username,
        'password': hashed_password,
        'name': name,
        'avatar': avatar,
        'bio': bio,
        'age': age,
        'car': car,
        'location': location,
        'team': team,
        'created_at': datetime.now(timezone.utc)
    }
    db_.users.insert_one(user_doc)
    return jsonify({"msg": "User registered successfully"}), 201

@users_bp.route('/login', methods=['POST'])
def login():
    db_ = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db_.users.find_one({'username': username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_logged_in_user():
    db_ = get_db()
    # JWT identity contains the username (set at login), so look up by username
    username = get_jwt_identity()
    user = db_.users.find_one(
        {'username': username},
        {'password': 0}
    )
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user['_id'] = str(user['_id'])
    return jsonify(user), 200