import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__) + "/..")
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY     = os.getenv("SECRET_KEY", "change_me_if_missing")
    MONGO_URI      = os.getenv("MONGO_URI")
    REDIS_URL      = os.getenv("REDIS_URL")
    SCHEDULER_API_ENABLED    = False
    JOBS = [
        {
        'id': 'sync_views',
        'func': 'app.tasks.sync_views:sync_views_job',
        'trigger': 'interval',
        'minutes': 10
        }
    ]

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv("MONGO_TEST_URI", "mongodb://localhost:27017/test_db")