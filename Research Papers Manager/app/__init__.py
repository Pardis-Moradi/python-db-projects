from flask import Flask
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import mongo, redis_client, bcrypt, scheduler

config_map = {
    "development": DevelopmentConfig,
    "testing":    TestingConfig,
    "production": ProductionConfig,
}

def create_app(config_name=None):
    app = Flask(__name__)

    # 1. Determine which config to load
    cfg = config_map.get(
        config_name or os.getenv("FLASK_ENV", "development")
    )
    app.config.from_object(cfg)

    # 2. Initialize extensions
    mongo.init_app(app)
    redis_client.init_app(app)
    bcrypt.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # 3. Register blueprints…
    from .controllers.auth      import auth_bp
    from .controllers.papers    import papers_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(papers_bp)

    return app
