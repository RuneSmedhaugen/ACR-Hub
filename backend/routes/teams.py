from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.connection import get_db
from bson import ObjectId
from datetime import datetime, timezone

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/', methods=['GET'])
def list_teams():
    try:
        db = get_db()
        teams = list(db.teams.find({}).sort('created_at', -1))

        for team in teams:
            team['_id'] = str(team['_id'])
            team['leader_id'] = str(team['leader_id'])
            member_count = db.team_members.count_documents({
                'team_id': ObjectId(team['_id'])
            })
            team['member_count'] = member_count

        return jsonify(teams), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>', methods=['GET'])
def get_team(team_id):
    try:
        db = get_db()
        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        team['_id'] = str(team['_id'])
        team['leader_id'] = str(team['leader_id'])

        members_docs = list(db.team_members.find({
            'team_id': ObjectId(team_id)
        }))

        members = []
        for member_doc in members_docs:
            user = db.users.find_one(
                {'_id': member_doc['user_id']},
                {'password': 0}
            )
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
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if user.get('team'):
            return jsonify({"msg": "You are already in a team"}), 400

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

        # Add creator as member
        db.team_members.insert_one({
            'team_id': result.inserted_id,
            'user_id': user['_id'],
            'joined_at': datetime.now(timezone.utc)
        })

        # Update user document
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'team': str(result.inserted_id)}}
        )

        return jsonify({
            "_id": str(result.inserted_id),
            "name": name,
            "description": description,
            "leader_id": str(user['_id'])
        }), 201

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_team(team_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if user.get('team'):
            return jsonify({"msg": "You are already in a team"}), 400

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        # Prevent duplicate applications
        if db.team_applications.find_one({
            'team_id': ObjectId(team_id),
            'user_id': user['_id'],
            'status': 'pending'
        }):
            return jsonify({"msg": "Application already pending"}), 400

        db.team_applications.insert_one({
            'team_id': ObjectId(team_id),
            'user_id': user['_id'],
            'status': 'pending',
            'applied_at': datetime.now(timezone.utc)
        })

        return jsonify({"msg": "Application submitted"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/applications', methods=['GET'])
@jwt_required()
def get_applications(team_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        leader = db.users.find_one({'username': username})

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        if team['leader_id'] != leader['_id']:
            return jsonify({"msg": "Only leader can view applications"}), 403

        apps = list(db.team_applications.find({
            'team_id': ObjectId(team_id),
            'status': 'pending'
        }))

        result = []
        for app in apps:
            user = db.users.find_one(
                {'_id': app['user_id']},
                {'password': 0}
            )
            if user:
                user['_id'] = str(user['_id'])
                result.append({
                    'application_id': str(app['_id']),
                    'user': user
                })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/applications/<application_id>/accept', methods=['POST'])
@jwt_required()
def accept_application(team_id, application_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        leader = db.users.find_one({'username': username})

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        if team['leader_id'] != leader['_id']:
            return jsonify({"msg": "Only team leader can accept applications"}), 403

        application = db.team_applications.find_one({
            '_id': ObjectId(application_id),
            'team_id': ObjectId(team_id),
            'status': 'pending'
        })

        if not application:
            return jsonify({"msg": "Application not found"}), 404

        user_id = application['user_id']

        # Add to team_members
        db.team_members.insert_one({
            'team_id': ObjectId(team_id),
            'user_id': user_id,
            'joined_at': datetime.now(timezone.utc)
        })

        # Update user team field
        db.users.update_one(
            {'_id': user_id},
            {'$set': {'team': str(team_id)}}
        )

        # Mark application accepted
        db.team_applications.update_one(
            {'_id': ObjectId(application_id)},
            {'$set': {'status': 'accepted'}}
        )

        return jsonify({"msg": "Application accepted"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/applications/<application_id>/reject', methods=['POST'])
@jwt_required()
def reject_application(team_id, application_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        leader = db.users.find_one({'username': username})

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        if team['leader_id'] != leader['_id']:
            return jsonify({"msg": "Only team leader can reject applications"}), 403

        db.team_applications.delete_one({
            '_id': ObjectId(application_id),
            'team_id': ObjectId(team_id)
        })

        return jsonify({"msg": "Application rejected"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>/leave', methods=['POST'])
@jwt_required()
def leave_team(team_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        if team['leader_id'] == user['_id']:
            return jsonify({"msg": "Team leader cannot leave team"}), 400

        db.team_members.delete_one({
            'team_id': ObjectId(team_id),
            'user_id': user['_id']
        })

        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'team': ''}}
        )

        return jsonify({"msg": "Successfully left team"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@teams_bp.route('/<team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    try:
        db = get_db()
        username = get_jwt_identity()
        user = db.users.find_one({'username': username})

        team = db.teams.find_one({'_id': ObjectId(team_id)})
        if not team:
            return jsonify({"msg": "Team not found"}), 404

        if team['leader_id'] != user['_id']:
            return jsonify({"msg": "Only team leader can delete team"}), 403

        db.teams.delete_one({'_id': ObjectId(team_id)})
        db.team_members.delete_many({'team_id': ObjectId(team_id)})
        db.team_applications.delete_many({'team_id': ObjectId(team_id)})

        # Clear team field for all users in that team
        db.users.update_many(
            {'team': team_id},
            {'$set': {'team': ''}}
        )

        return jsonify({"msg": "Team deleted successfully"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
