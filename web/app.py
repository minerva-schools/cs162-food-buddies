from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import Blueprint
from flask import current_app as app
from .models import db, City, Cuisine, DineTime

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
    return render_template('preference.html', firstName=current_user.first_name.capitalize())
    #For getting the mealTime use the following line
    #request.form.get ("mealTime")
    #For getting the dietary preferences use the following line
    #request.form.getlist ("dietary")
    #For getting the Availability time from, use the following line
    #request.form.get ("ava_from")
    #For getting the Availability time to, use the following line
    #request.form.get ("ava_to")
