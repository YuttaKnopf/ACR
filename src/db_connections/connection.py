import os
from pymongo import MongoClient


def mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    return MongoClient(mongo_uri)


def connect():
    try:
        client = mongo_client()
        mongo_db = os.getenv("MONGODB_DATABASE")
        db = client[mongo_db]
        return db
    except Exception as e:
        raise Exception(f"An error occurred during database connection: {e}")


def disconnect():
    try:
        client = mongo_client()
        client.close()
    except Exception:
        return
