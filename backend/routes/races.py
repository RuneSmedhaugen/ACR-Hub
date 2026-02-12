from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.connection import get_db
from bson import ObjectId
from datetime import datetime, timezone

races_bp = Blueprint('races', __name__)

# ----------------------------------
# CONFIG DATA (Hardcoded Structure)
# ----------------------------------

RALLIES = {
    "Rally Alsace": {
        "Vallèe de Munster": list(range(1, 7)),
        "Saverne": list(range(1, 5)),
    },
    "Livigno Circuit": {
        "Ice Track": list(range(1, 3)),
    },
    "Wales": {
        "Hafren North": list(range(1, 7)),
        "Hafren South": list(range(1, 3)),
    }
}

GROUPS = ["2/4", "A", "R", "WR", "B"]

CLASSES = [
    "H1", "H2", "H3",
    "A8 Evo2",
    "Rally2",
    "Evo2",
    "Rally4",
    "B2"
]

CARS = [
    {"name": "Xsata WRC - 2003", "group": "WR", "class": "Evo2"},
    {"name": "i20 Rally2 - 2021", "group": "R", "class": "Rally2"},
    {"name": "Stratos HF - 1976", "group": "2/4", "class": "H1"},
    {"name": "131 Abarth - 1976", "group": "2/4", "class": "H1"},
    {"name": "Rally 037 Evoluzione 2 - 1984", "group": "B", "class": "B2"},
    {"name": "124 Abarth Rally 16V - 1974", "group": "2/4", "class": "H2"},
    {"name": "Delta Integrale Evoluzione - 1992", "group": "A", "class": "A8 Evo2"},
    {"name": "GTA 1300 Junior - 1972", "group": "2/4", "class": "H3"},
    {"name": "208 Rally4 - 2020", "group": "R", "class": "Rally4"},
    {"name": "A110 1.8 - 1973", "group": "2/4", "class": "H2"},
    {"name": "Mini Cooper S - 1964", "group": "2/4", "class": "H3"},
]

# ----------------------------------
# LIST RACES
# ----------------------------------

@races_bp.route('/', methods=['GET'])
def list_races():
    db = get_db()
    races = list(db.races.find({}).sort('created_at', -1))

    for race in races:
        race['_id'] = str(race['_id'])
        race['created_by'] = str(race['created_by'])

    return jsonify(races), 200


# ----------------------------------
# GET SINGLE RACE
# ----------------------------------

@races_bp.route('/<race_id>', methods=['GET'])
def get_race(race_id):
    db = get_db()
    race = db.races.find_one({'_id': ObjectId(race_id)})

    if not race:
        return jsonify({"msg": "Race not found"}), 404

    race['_id'] = str(race['_id'])
    race['created_by'] = str(race['created_by'])

    # participants
    participants = list(db.race_participants.find({
        'race_id': ObjectId(race_id)
    }))

    enriched = []
    for p in participants:
        user = db.users.find_one({'_id': p['user_id']}, {'password': 0})
        if user:
            user['_id'] = str(user['_id'])
            enriched.append(user)

    race['participants'] = enriched

    return jsonify(race), 200


# ----------------------------------
# CREATE RACE
# ----------------------------------

@races_bp.route('/', methods=['POST'])
@jwt_required()
def create_race():
    db = get_db()
    username = get_jwt_identity()
    user = db.users.find_one({'username': username})

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    rally = data.get('rally')
    stage = data.get('stage')
    variant = data.get('variant')
    group = data.get('group')
    race_class = data.get('class')  # optional
    car = data.get('car')  # optional
    description = data.get('description', '')

    # ---- VALIDATION ----

    if rally not in RALLIES:
        return jsonify({"msg": "Invalid rally"}), 400

    if stage not in RALLIES[rally]:
        return jsonify({"msg": "Invalid stage for selected rally"}), 400

    if variant not in RALLIES[rally][stage]:
        return jsonify({"msg": "Invalid variant for selected stage"}), 400

    if group not in GROUPS:
        return jsonify({"msg": "Invalid group"}), 400

    if race_class and race_class not in CLASSES:
        return jsonify({"msg": "Invalid class"}), 400

    if car:
        valid_car = next((c for c in CARS if c['name'] == car), None)
        if not valid_car:
            return jsonify({"msg": "Invalid car"}), 400
        if valid_car['group'] != group:
            return jsonify({"msg": "Car does not match selected group"}), 400
        if race_class and valid_car['class'] != race_class:
            return jsonify({"msg": "Car does not match selected class"}), 400

    race_doc = {
        "rally": rally,
        "stage": stage,
        "variant": variant,
        "group": group,
        "class": race_class,
        "car": car,
        "description": description,
        "created_by": user['_id'],
        "created_at": datetime.now(timezone.utc)
    }

    result = db.races.insert_one(race_doc)

    return jsonify({
        "_id": str(result.inserted_id),
        **race_doc,
        "created_by": str(race_doc['created_by'])
    }), 201


# ----------------------------------
# JOIN RACE
# ----------------------------------

@races_bp.route('/<race_id>/join', methods=['POST'])
@jwt_required()
def join_race(race_id):
    db = get_db()
    username = get_jwt_identity()
    user = db.users.find_one({'username': username})

    race = db.races.find_one({'_id': ObjectId(race_id)})
    if not race:
        return jsonify({"msg": "Race not found"}), 404

    if db.race_participants.find_one({
        'race_id': ObjectId(race_id),
        'user_id': user['_id']
    }):
        return jsonify({"msg": "Already joined"}), 400

    db.race_participants.insert_one({
        "race_id": ObjectId(race_id),
        "user_id": user['_id'],
        "joined_at": datetime.now(timezone.utc)
    })

    return jsonify({"msg": "Joined race"}), 200


# ----------------------------------
# SUBMIT TIME
# ----------------------------------

@races_bp.route('/<race_id>/submit-time', methods=['POST'])
@jwt_required()
def submit_time(race_id):
    db = get_db()
    username = get_jwt_identity()
    user = db.users.find_one({'username': username})

    race = db.races.find_one({'_id': ObjectId(race_id)})
    if not race:
        return jsonify({"msg": "Race not found"}), 404

    # must be participant
    if not db.race_participants.find_one({
        'race_id': ObjectId(race_id),
        'user_id': user['_id']
    }):
        return jsonify({"msg": "You must join the race first"}), 403

    data = request.get_json()
    time_ms = data.get('time')

    if not isinstance(time_ms, (int, float)) or time_ms <= 0:
        return jsonify({"msg": "Valid time required"}), 400

    db.race_times.insert_one({
        "race_id": ObjectId(race_id),
        "user_id": user['_id'],
        "time_ms": time_ms,
        "submitted_at": datetime.now(timezone.utc)
    })

    return jsonify({"msg": "Time submitted"}), 201


# ----------------------------------
# GET TIMES (LEADERBOARD)
# ----------------------------------

@races_bp.route('/<race_id>/times', methods=['GET'])
def get_times(race_id):
    db = get_db()

    times = list(db.race_times.find({
        'race_id': ObjectId(race_id)
    }).sort('time_ms', 1))

    leaderboard = []

    for idx, entry in enumerate(times):
        user = db.users.find_one({'_id': entry['user_id']}, {'password': 0})
        if user:
            user['_id'] = str(user['_id'])
            leaderboard.append({
                "rank": idx + 1,
                "user": user,
                "time": entry['time_ms']
            })

    return jsonify(leaderboard), 200


# ----------------------------------
# DELETE RACE
# ----------------------------------

@races_bp.route('/<race_id>', methods=['DELETE'])
@jwt_required()
def delete_race(race_id):
    db = get_db()
    username = get_jwt_identity()
    user = db.users.find_one({'username': username})

    race = db.races.find_one({'_id': ObjectId(race_id)})
    if not race:
        return jsonify({"msg": "Race not found"}), 404

    if race['created_by'] != user['_id']:
        return jsonify({"msg": "Only creator can delete"}), 403

    db.race_participants.delete_many({'race_id': ObjectId(race_id)})
    db.race_times.delete_many({'race_id': ObjectId(race_id)})
    db.races.delete_one({'_id': ObjectId(race_id)})

    return jsonify({"msg": "Race deleted"}), 200
