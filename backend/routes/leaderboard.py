from flask import Blueprint, request, jsonify
from db.connection import get_db
from bson import ObjectId

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/races/<race_id>', methods=['GET'])
def get_race_leaderboard(race_id):
    """Get leaderboard for a specific race, ranked by cumulative stage times."""
    try:
        db = get_db()
        
        # Validate race exists
        race = db.races.find_one({'_id': ObjectId(race_id)})
        if not race:
            return jsonify({"msg": "Race not found"}), 404
        
        # Aggregate stage times for this race
        pipeline = [
            {'$match': {'race_id': ObjectId(race_id)}},
            {'$group': {
                '_id': '$user_id',
                'total_time': {'$sum': '$time_ms'},
                'stage_count': {'$sum': 1},
                'best_stage': {'$min': '$time_ms'}
            }},
            {'$sort': {'total_time': 1}},
            {'$limit': 1000}
        ]
        
        results = list(db.stage_times.aggregate(pipeline))
        
        # Enrich with user info
        leaderboard = []
        for idx, entry in enumerate(results):
            user = db.users.find_one({'_id': ObjectId(entry['_id'])}, {'password': 0})
            if user:
                user['_id'] = str(user['_id'])
                leaderboard.append({
                    'rank': idx + 1,
                    'user': user,
                    'total_time': entry['total_time'],
                    'stage_count': entry['stage_count'],
                    'best_stage': entry['best_stage']
                })
        
        return jsonify({
            'race': {
                '_id': str(race['_id']),
                'name': race.get('name'),
                'track': race.get('track'),
                'surface': race.get('surface'),
                'class': race.get('class')
            },
            'leaderboard': leaderboard
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@leaderboard_bp.route('/races/<race_id>/stages', methods=['GET'])
def get_race_stages_leaderboard(race_id):
    """Get breakdown of each stage within a race with rankings."""
    try:
        db = get_db()
        
        race = db.races.find_one({'_id': ObjectId(race_id)})
        if not race:
            return jsonify({"msg": "Race not found"}), 404
        
        stages = list(db.stages.find({'race_id': ObjectId(race_id)}).sort('order', 1))
        
        stages_leaderboard = []
        for stage in stages:
            # Get top 10 times for this stage
            pipeline = [
                {'$match': {'stage_id': ObjectId(stage['_id'])}},
                {'$sort': {'time_ms': 1}},
                {'$limit': 10}
            ]
            
            stage_times = list(db.stage_times.aggregate(pipeline))
            
            entries = []
            for idx, time_entry in enumerate(stage_times):
                user = db.users.find_one({'_id': ObjectId(time_entry['user_id'])}, {'password': 0})
                if user:
                    user['_id'] = str(user['_id'])
                    entries.append({
                        'rank': idx + 1,
                        'user': user,
                        'time': time_entry['time_ms'],
                        'submitted_at': time_entry.get('submitted_at')
                    })
            
            stages_leaderboard.append({
                'stage': {
                    '_id': str(stage['_id']),
                    'name': stage.get('name'),
                    'track': stage.get('track'),
                    'surface': stage.get('surface'),
                    'order': stage.get('order')
                },
                'times': entries
            })
        
        return jsonify({
            'race': {
                '_id': str(race['_id']),
                'name': race.get('name')
            },
            'stages': stages_leaderboard
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@leaderboard_bp.route('/user/<user_id>', methods=['GET'])
def get_user_times(user_id):
    """Get all times for a specific user across all races."""
    try:
        db = get_db()
        
        user = db.users.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        user['_id'] = str(user['_id'])
        
        # Get all stage times
        times = list(db.stage_times.find(
            {'user_id': ObjectId(user_id)}
        ).sort('submitted_at', -1))
        
        user_times_enriched = []
        for time_entry in times:
            race = db.races.find_one({'_id': ObjectId(time_entry['race_id'])})
            stage = db.stages.find_one({'_id': ObjectId(time_entry['stage_id'])})
            
            user_times_enriched.append({
                '_id': str(time_entry['_id']),
                'race': {
                    '_id': str(race['_id']),
                    'name': race.get('name')
                } if race else None,
                'stage': {
                    '_id': str(stage['_id']),
                    'name': stage.get('name')
                } if stage else None,
                'time': time_entry['time_ms'],
                'submitted_at': time_entry.get('submitted_at')
            })
        
        return jsonify({
            'user': user,
            'times': user_times_enriched
        }), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
