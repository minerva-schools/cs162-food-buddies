from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import Blueprint
from flask import current_app as app
from datetime import datetime
from .models import db, User, City, Cuisine, Preference, DineTime

# create an app factory
main_routes = Blueprint('main_route',__name__,template_folder='templates')

# define event listeners
# * each lister inserts default data to the specified table (only once) after db creation
@db.event.listens_for(City.__table__, 'after_create', once=True)
def insert_city_options(*args, **kwargs):
    '''insert Minerva city options upon db creation'''
    MinervaCities = ['San Francisco', 'Seoul', 'Hyderabad', 'Berlin', 'Buenos Aires', 'London', 'Taipei']
    for city_name in MinervaCities:
         db.session.add(City(city_name=city_name))
    db.session.commit()

@db.event.listens_for(Cuisine.__table__, 'after_create', once=True)
def insert_cuisine_options(*args, **kwargs):
    '''insert cuisine options upon db creation'''
    CuisineTypes = ['American', 'Asian', 'European', 'Middle Eastern', 'Latin American', 'Subcontinental']
    for cuisine_name in CuisineTypes:
        db.session.add(Cuisine(cuisine_name=cuisine_name))
    db.session.commit()

@db.event.listens_for(DineTime.__table__, 'after_create', once=True)
def insert_dinetime_options(*args, **kwargs):
    '''insert dining time options upon db creation'''
    DiningTimes = ['Lunch', 'Dinner', 'Breakfast']
    for dinetime_name in DiningTimes:
        db.session.add(DineTime(dinetime_name=dinetime_name))
    db.session.commit()



# placeholder reference to homepage
@main_routes.route('/')
def index():

    return render_template('login.html')

@main_routes.route('/preference', methods=['GET','POST'])
@login_required
def preference():
    if request.method == 'GET':
        return render_template('preference.html', firstName=current_user.first_name.capitalize())
    elif request.method == 'POST':
        # check whether user preferences are already set
        preference = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()
        if preference: # update preferences
            # determine linking to other tables
            cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name==request.form.get('cuisine_selected')).first()
            dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name==request.form.get('mealTime')).first()
            #update values
            preference.date_time = datetime.now()
            preference.cuisine_id = 1 # placeholder -- change to cuisine.id
            preference.dinetime_id = dinetime.id
            preference.require_vegetarian = ("vegetarian" in request.form)
            preference.require_vegan = ("vegan" in request.form)
            preference.require_halal = ("halal" in request.form)
            preference.require_gluten_free = ("glutenFree" in request.form)
            preference.require_dairy_free = ("dairyFree" in request.form)
            preference.start_time = request.form['ava_from']
            preference.end_time = request.form['ava_to']
            db.session.commit()

        else: # set user preferences
            # determine linking to other tables
            cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name==request.form.get('cuisine_selected')).first()
            dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name==request.form.get('mealTime')).first()
            #placeholder cuisine - change to cuisine.id
            preference = Preference(date_time=datetime.now(), user_id=current_user.id, cuisine_id=1, dinetime_id=dinetime.id, city_id=current_user.city_id, require_vegetarian=("vegetarian" in request.form),require_vegan=("vegan" in request.form),require_halal=("halal" in request.form),require_gluten_free=("glutenFree" in request.form),require_dairy_free=("dairyFree" in request.form),start_time=request.form['ava_from'],end_time=request.form['ava_to'])
            db.session.add(preference)
            db.session.commit()
        # return redirect(url_for('main_route.results'))

    #For getting the mealTime use the following line
    #request.form.get ("mealTime")
    #For getting the dietary preferences use the following line
    #request.form.getlist ("dietary")
    #For getting the Availability time from, use the following line
    #request.form.get ("ava_from")
    #For getting the Availability time to, use the following line
    #request.form.get ("ava_to")
