from flask import Flask,render_template,url_for, flash,redirect
from flask_login import LoginManager
import os
from .config import config_by_name
from web.models import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

login_manager = LoginManager()
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def custom_401(e):
     flash('You need to login for accessing this page!')
     return redirect(url_for('authentication.login'))

def create_app(config_name='dev'):
    app = Flask(__name__)

    config_name = os.environ.get('FLASK_CONFIG', config_name)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, custom_401)

    with app.app_context():
        from web.authentication import authentication
        app.register_blueprint(authentication, url_prefix="/")
        from web.app import main_routes
        app.register_blueprint(main_routes,url_prefix='/')

        # Create DB Models
        # db.create_all()

    return app
