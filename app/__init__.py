from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import mapping_config


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(mapping_config[config_name])


    # database
    db.init_app(app)

    # blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app