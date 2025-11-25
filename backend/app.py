from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGNO_URI"))
db = client["rallyhub"]

@app.route("/)")
def home():
    return jsonify({"message": "Welcome to the ACR Hub Backend!"})

if __name__ == "__main__":
    app.run(debug=True)