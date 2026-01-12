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


@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_logged_in_user():
    try:
        db_ = get_db()
        current_username = get_jwt_identity()
        user = db_.users.find_one({'username': current_username})
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json() or {}
        update = {}
        allowed = ('username', 'name', 'avatar', 'bio', 'age', 'car', 'location', 'team')

        # Basic validation and sanitization
        if 'username' in data:
            new_username = (data.get('username') or '').strip()
            if not new_username or len(new_username) < 3:
                return jsonify({"msg": "Username must be at least 3 characters"}), 400
            # check uniqueness
            if new_username != current_username and db_.users.find_one({'username': new_username}):
                return jsonify({"msg": "Username already exists"}), 400
            update['username'] = new_username

        if 'name' in data:
            name = (data.get('name') or '').strip()
            if len(name) > 100:
                return jsonify({"msg": "Name too long"}), 400
            update['name'] = name

        if 'avatar' in data:
            avatar = (data.get('avatar') or '').strip()
            if avatar and not (avatar.startswith('http://') or avatar.startswith('https://')):
                return jsonify({"msg": "Avatar must be a valid URL"}), 400
            update['avatar'] = avatar

        if 'bio' in data:
            bio = (data.get('bio') or '').strip()
            if len(bio) > 1000:
                return jsonify({"msg": "Bio too long"}), 400
            update['bio'] = bio

        if 'age' in data:
            try:
                age = int(data.get('age') or 0)
                if age < 0:
                    return jsonify({"msg": "Age must be non-negative"}), 400
                update['age'] = age
            except Exception:
                return jsonify({"msg": "Invalid age"}), 400

        if 'car' in data:
            car = (data.get('car') or '').strip()
            if len(car) > 200:
                return jsonify({"msg": "Car description too long"}), 400
            update['car'] = car

        if 'location' in data:
            location = (data.get('location') or '').strip()
            if len(location) > 200:
                return jsonify({"msg": "Location too long"}), 400
            update['location'] = location

        if 'team' in data:
            update['team'] = data.get('team')

        access_token = None
        if update:
            update['updated_at'] = datetime.now(timezone.utc)
            db_.users.update_one({'_id': user['_id']}, {'$set': update})

            # If username changed, issue a new access token
            if 'username' in update and update['username'] != current_username:
                access_token = create_access_token(identity=update['username'])

        # Return only the updated fields (and new token if generated)
        resp = {'updated': update}
        if access_token:
            resp['access_token'] = access_token

        return jsonify(resp), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500