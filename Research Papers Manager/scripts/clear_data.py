#!/usr/bin/env python3
import os
from pymongo import MongoClient
import redis
from dotenv import load_dotenv

load_dotenv()

# Load connection settings
MONGO_URI   = os.getenv("MONGO_URI", "mongodb://localhost:27017")
REDIS_URL   = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DB_NAME     = os.getenv("MONGO_DB", "research_manager")

def clear_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    # Drop specific collections
    for col in ["users", "papers", "citations"]:
        if col in db.list_collection_names():
            db.drop_collection(col)
            print(f"Dropped MongoDB collection: {col}")
    client.close()

def clear_redis():
    r = redis.from_url(REDIS_URL)
    # Remove all keys related to our app
    keys = r.keys("usernames") + r.keys("search:*") + r.keys("paper_views:*")
    if keys:
        r.delete(*keys)
        print(f"Deleted Redis keys: {keys}")
    else:
        print("No matching Redis keys found.")

if __name__ == "__main__":
    clear_mongo()
    clear_redis()
    print("Database cleanup complete.")

