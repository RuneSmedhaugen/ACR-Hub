from flask import current_app, g
from pymongo import MongoClient

def get_db():
    if 'db' not in g:
        g.db = MongoClient(current_app.config["MONGNO_URI"]).rallyhub
    return g.db