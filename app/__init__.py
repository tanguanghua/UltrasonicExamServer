from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import mapping_config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    config = mapping_config[config_name]
    app.config.from_object(config)

    # database
    db.init_app(app)
    if config.NUM_TESTS:
        db.NUM_TESTS = config.NUM_TESTS
    else:
        db.NUM_TESTS = 10

    # blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
