from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from routes.users import users_bp
from routes.leaderboard import leaderboard_bp
from routes.teams import teams_bp
from routes.races import races_bp

from db.connection import get_db

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
app.register_blueprint(teams_bp, url_prefix='/teams')
app.register_blueprint(races_bp, url_prefix='/races')

@app.route("/")
def home():
    db = get_db()
    return jsonify({
        "message": "Backend running",
        "collections": db.list_collection_names()
    })



if __name__ == "__main__":
    app.run(debug=True)
