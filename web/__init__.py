from flask import Flask,render_template,url_for, flash,redirect
from flask_login import LoginManager
import os
from .config import config_by_name
from web.models import db, City, Cuisine, DineTime
from web.utils import mail

#from web.initial_values import insert_defaults
#from sqlalchemy.event import listen
#def insert_city_options(*args, **kwargs):
#    MinervaCities = ['San Francisco', 'Seoul', 'Hyderabad', 'Berlin',       'Buenos Aires', 'London', 'Taipei']
#    for city_name in MinervaCities:
#        db.session.add(City(city_name=city_name))
#

## hack: default value insertion upon db creation
#global DEFAULTS_INSERTED
#DEFAULTS_INSERTED = 0

login_manager = LoginManager()

def page_not_found(e):
    return render_template('404.html'), 404

def custom_401(e):
     flash('You need to login for accessing this page!', "error")
     return redirect(url_for('authentication.login'))

def create_app(config_name='dev'):
    global DEFAULTS_INSERTED
    
    app = Flask(__name__)

    config_name = os.environ.get('FLASK_CONFIG', config_name)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, custom_401)

    with app.app_context():
    
        from web.authentication import authentication
        app.register_blueprint(authentication, url_prefix="/")
        from web.app import main_routes
        app.register_blueprint(main_routes,url_prefix='/')

        # Create DB Models
        db.create_all()
        
#        listen(City.__table__, 'connect', insert_city_options, once=True)
#        # another function to wait(listen to) for db creation
#        # insert default values upon db creation
#        if DEFAULTS_INSERTED==0:
#
#            MinervaCities = ['San Francisco', 'Seoul', 'Hyderabad', 'Berlin',       'Buenos Aires', 'London', 'Taipei']
#            for city_name in MinervaCities:
#                db.session.add(City(city_name=city_name))
#
#            CuisineTypes = ['Asian', 'American', 'Subcontinental', 'European']
#            for cuisine_name in CuisineTypes:
#                db.session.add(Cuisine(cuisine_name=cuisine_name))
#
#            DiningTimes = ['Lunch', 'Dinner', 'Breakfast']
#            for dinetime_name in DiningTimes:
#                db.session.add(DineTime(dinetime_name=dinetime_name))
#
#            db.session.commit()
#            # update status to prevent dulicated insertions
#            DEFAULTS_INSERTED += 1

        
    return app
