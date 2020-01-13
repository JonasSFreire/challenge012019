from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from app.api.resources import api_bp
    app.register_blueprint(api_bp, url_prefix='/v1')

    return app