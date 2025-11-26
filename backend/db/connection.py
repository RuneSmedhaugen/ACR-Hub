from flask import current_app, g
from pymongo import MongoClient
import os

def get_db():
    if 'db' not in g:
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME")
        client = MongoClient(mongo_uri)
        g.db = client[db_name]
    return g.db