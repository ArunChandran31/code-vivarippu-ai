# backend/db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

_db = None
DEFAULT_DB_NAME = "ai_code_reviewer"

def init_db(uri=None):
    global _db
    uri = uri or os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(uri)
    try:
        db = client.get_default_database()
    except Exception:
        db = None

    if db is None:
        db = client[DEFAULT_DB_NAME]

    _db = db


def get_db():
    if _db is None:
        raise RuntimeError("DB not initialized. Call init_db() first.")
    return _db
