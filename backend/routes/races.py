from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.connection import get_db
from bson import ObjectId
from datetime import datetime, timezone

races_bp = Blueprint('races', __name__)

@races_bp.route('/', methods=['GET'])
def list_races():
    """Get all races."""
    try:
        db = get_db()
        races = list(db.races.find({}).sort('created_at', -1))
        
        for race in races:
            race['_id'] = str(race['_id'])
            race['created_by'] = str(race['created_by'])
        
        return jsonify(races), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/<race_id>', methods=['GET'])
def get_race(race_id):
    """Get race details with all stages."""
    try:
        db = get_db()
        race = db.races.find_one({'_id': ObjectId(race_id)})
        if not race:
            return jsonify({"msg": "Race not found"}), 404
        
        race['_id'] = str(race['_id'])
        race['created_by'] = str(race['created_by'])
        
        # Get all stages
        stages = list(db.stages.find({'race_id': ObjectId(race_id)}).sort('order', 1))
        for stage in stages:
            stage['_id'] = str(stage['_id'])
            stage['race_id'] = str(stage['race_id'])
        
        race['stages'] = stages
        
        return jsonify(race), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/', methods=['POST'])
@jwt_required()
def create_race():
    """Create a new race."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        data = request.get_json()
        name = data.get('name')
        track = data.get('track', '')
        surface = data.get('surface', '')
        race_class = data.get('class', '')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"msg": "Race name required"}), 400
        
        race_doc = {
            'name': name,
            'track': track,
            'surface': surface,
            'class': race_class,
            'description': description,
            'created_by': user['_id'],
            'created_at': datetime.now(timezone.utc)
        }
        result = db.races.insert_one(race_doc)
        
        return jsonify({
            "_id": str(result.inserted_id),
            **race_doc,
            "created_by": str(race_doc['created_by'])
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/<race_id>/stages', methods=['POST'])
@jwt_required()
def add_stage(race_id):
    """Add a stage to a race."""
    try:
        db = get_db()
        
        race = db.races.find_one({'_id': ObjectId(race_id)})
        if not race:
            return jsonify({"msg": "Race not found"}), 404
        
        data = request.get_json()
        name = data.get('name')
        track = data.get('track', '')
        surface = data.get('surface', '')
        order = data.get('order', 1)
        description = data.get('description', '')
        
        if not name:
            return jsonify({"msg": "Stage name required"}), 400
        
        stage_doc = {
            'race_id': ObjectId(race_id),
            'name': name,
            'track': track,
            'surface': surface,
            'order': order,
            'description': description,
            'created_at': datetime.now(timezone.utc)
        }
        result = db.stages.insert_one(stage_doc)
        
        return jsonify({
            "_id": str(result.inserted_id),
            "race_id": str(stage_doc['race_id']),
            **{k: v for k, v in stage_doc.items() if k != 'race_id'}
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/stages/<stage_id>/submit-time', methods=['POST'])
@jwt_required()
def submit_stage_time(stage_id):
    """Submit a time for a stage."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        stage = db.stages.find_one({'_id': ObjectId(stage_id)})
        if not stage:
            return jsonify({"msg": "Stage not found"}), 404
        
        data = request.get_json()
        time_ms = data.get('time')  # Time in milliseconds
        
        if not isinstance(time_ms, (int, float)) or time_ms <= 0:
            return jsonify({"msg": "Valid time required"}), 400
        
        time_entry = {
            'race_id': stage['race_id'],
            'stage_id': ObjectId(stage_id),
            'user_id': user['_id'],
            'time_ms': time_ms,
            'submitted_at': datetime.now(timezone.utc)
        }
        result = db.stage_times.insert_one(time_entry)
        
        return jsonify({
            "_id": str(result.inserted_id),
            **time_entry,
            "race_id": str(time_entry['race_id']),
            "stage_id": str(time_entry['stage_id']),
            "user_id": str(time_entry['user_id'])
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/stages/<stage_id>/times', methods=['GET'])
def get_stage_times(stage_id):
    """Get all times submitted for a stage."""
    try:
        db = get_db()
        
        stage = db.stages.find_one({'_id': ObjectId(stage_id)})
        if not stage:
            return jsonify({"msg": "Stage not found"}), 404
        
        times = list(db.stage_times.find(
            {'stage_id': ObjectId(stage_id)}
        ).sort('time_ms', 1))
        
        times_enriched = []
        for idx, time_entry in enumerate(times):
            user = db.users.find_one({'_id': ObjectId(time_entry['user_id'])}, {'password': 0})
            if user:
                user['_id'] = str(user['_id'])
                times_enriched.append({
                    'rank': idx + 1,
                    '_id': str(time_entry['_id']),
                    'user': user,
                    'time': time_entry['time_ms'],
                    'submitted_at': time_entry['submitted_at']
                })
        
        return jsonify({
            'stage': {
                '_id': str(stage['_id']),
                'name': stage.get('name'),
                'track': stage.get('track'),
                'surface': stage.get('surface')
            },
            'times': times_enriched
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@races_bp.route('/<race_id>', methods=['DELETE'])
@jwt_required()
def delete_race(race_id):
    """Delete a race (creator only)."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        race = db.races.find_one({'_id': ObjectId(race_id)})
        if not race:
            return jsonify({"msg": "Race not found"}), 404
        
        if race['created_by'] != user['_id']:
            return jsonify({"msg": "Only race creator can delete race"}), 403
        
        # Delete associated stages and times
        stages = db.stages.find({'race_id': ObjectId(race_id)})
        stage_ids = [stage['_id'] for stage in stages]
        
        db.stage_times.delete_many({'stage_id': {'$in': stage_ids}})
        db.stages.delete_many({'race_id': ObjectId(race_id)})
        db.races.delete_one({'_id': ObjectId(race_id)})
        
        return jsonify({"msg": "Race deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
