from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from db.connection import get_db

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

@app.route("/")
def home():
    db = get_db()
    return jsonify({
        "message": "Backend running",
        "collections": db.list_collection_names()
    })

if __name__ == "__main__":
    app.run(debug=True)
