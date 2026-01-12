from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.connection import get_db
from bson import ObjectId
from datetime import datetime, timezone

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/', methods=['GET'])
def list_teams():
    """Get all teams."""
    try:
        db = get_db()
        teams = list(db.teams.find({}).sort('created_at', -1))
        
        for team in teams:
            team['_id'] = str(team['_id'])
            team['leader_id'] = str(team['leader_id'])
            
            # Count members
            member_count = db.team_members.count_documents({'team_id': ObjectId(team['_id'])})
            team['member_count'] = member_count
        
        return jsonify(teams), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>', methods=['GET'])
def get_team(team_id):
    """Get team details with members."""
    try:
        db = get_db()
        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404
        
        team['_id'] = str(team['_id'])
        team['leader_id'] = str(team['leader_id'])
        
        # Get all members
        members_docs = list(db.team_members.find({'team_id': ObjectId(team_id)}))
        members = []
        for member_doc in members_docs:
            user = db.users.find_one({'_id': ObjectId(member_doc['user_id'])}, {'password': 0})
            if user:
                user['_id'] = str(user['_id'])
                members.append(user)
        
        team['members'] = members
        
        return jsonify(team), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/', methods=['POST'])
@jwt_required()
def create_team():
    """Create a new team."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({"msg": "Team name required"}), 400
        
        if db.teams.find_one({'name': name}):
            return jsonify({"msg": "Team name already exists"}), 400
        
        team_doc = {
            'name': name,
            'description': description,
            'leader_id': user['_id'],
            'created_at': datetime.now(timezone.utc)
        }
        result = db.teams.insert_one(team_doc)
        
        # Add creator as first member
        db.team_members.insert_one({
            'team_id': result.inserted_id,
            'user_id': user['_id'],
            'joined_at': datetime.now(timezone.utc)
        })
        
        return jsonify({
            "_id": str(result.inserted_id),
            "name": name,
            "description": description,
            "leader_id": str(user['_id']),
            "created_at": team_doc['created_at']
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/join', methods=['POST'])
@jwt_required()
def join_team(team_id):
    """Join a team."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404
        
        # Check if already a member
        if db.team_members.find_one({'team_id': ObjectId(team_id), 'user_id': user['_id']}):
            return jsonify({"msg": "Already a member of this team"}), 400
        
        db.team_members.insert_one({
            'team_id': ObjectId(team_id),
            'user_id': user['_id'],
            'joined_at': datetime.now(timezone.utc)
        })
        
        return jsonify({"msg": "Successfully joined team"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/leave', methods=['POST'])
@jwt_required()
def leave_team(team_id):
    """Leave a team."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404
        
        # Can't leave if you're the leader
        if team['leader_id'] == user['_id']:
            return jsonify({"msg": "Team leader cannot leave team"}), 400
        
        db.team_members.delete_one({
            'team_id': ObjectId(team_id),
            'user_id': user['_id']
        })
        
        return jsonify({"msg": "Successfully left team"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    """Delete a team (leader only)."""
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404
        
        if team['leader_id'] != user['_id']:
            return jsonify({"msg": "Only team leader can delete team"}), 403
        
        db.teams.delete_one({'_id': ObjectId(team_id)})
        db.team_members.delete_many({'team_id': ObjectId(team_id)})
        
        return jsonify({"msg": "Team deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
