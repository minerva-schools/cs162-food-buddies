from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import Blueprint
from flask import current_app as app
#from .models import db, User

# create an app factory
main_routes = Blueprint('main_route',__name__,template_folder='templates')


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
    
@@main_routes.route('/followup', methods=['GET','POST'])
@login_required
def followup():
    return render_template('followup.html', firstName=current_user.first_name.capitalize())
