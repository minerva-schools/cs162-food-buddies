from flask import Flask
from flask_login import LoginManager
import os
from .config import config_by_name
from web.models import db

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)

    config_name = os.environ.get('FLASK_CONFIG', config_name)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from web.authentication import authentication
        app.register_blueprint(authentication, url_prefix="/")
        from web.app import main_routes
        app.register_blueprint(main_routes,url_prefix='/')

        # Create DB Models
        db.create_all()

    return app
