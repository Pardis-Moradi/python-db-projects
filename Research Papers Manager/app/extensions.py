import os
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler
from redis import Redis

mongo      = PyMongo()
bcrypt     = Bcrypt()
scheduler  = APScheduler()

class FlaskRedis:
    """
    A tiny wrapper so that redis_client.init_app(app) works.
    Delegates all other attributes to the actual Redis client.
    """
    def __init__(self):
        self.client = None

    def init_app(self, app):
        # Read REDIS_URL from app.config
        url = app.config.get("REDIS_URL")
        if not url:
            raise RuntimeError("REDIS_URL not configured")
        self.client = Redis.from_url(url)

    def __getattr__(self, name):
        # Delegate everything else to the real client
        return getattr(self.client, name)

# instantiate one global redis_client
redis_client = FlaskRedis()
