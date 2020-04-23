from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import Blueprint
from flask import current_app as app
from datetime import datetime
from .models import db, User, City, Cuisine, Preference, DineTime

# create an app factory
main_routes = Blueprint('main_route',__name__,template_folder='templates')

# placeholder reference to homepage
@main_routes.route('/')
def index():
    return render_template('login.html')

@main_routes.route('/preference', methods=['GET','POST'])
@login_required
def preference():
    if request.method == 'GET':
        return render_template('preference.html', firstName=current_user.first_name.capitalize(),
        lastName=current_user.last_name.capitalize(),email=current_user.email,contactInfo=current_user.contact_info)
    elif request.method == 'POST':
        # check whether user preferences are already set
        preference = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()
        if preference: # update preferences
            # determine linking to other tables
            cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name==request.form.get('cuisine_selected')).first()
            dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name==request.form.get('mealTime')).first()
            #update values
            preference.date_time = datetime.utcnow()
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
            preference = Preference(date_time=datetime.utcnow(), user_id=current_user.id, cuisine_id=1, dinetime_id=dinetime.id, city_id=current_user.city_id, require_vegetarian=("vegetarian" in request.form),require_vegan=("vegan" in request.form),require_halal=("halal" in request.form),require_gluten_free=("glutenFree" in request.form),require_dairy_free=("dairyFree" in request.form),start_time=request.form['ava_from'],end_time=request.form['ava_to'])
            db.session.add(preference)
            db.session.commit()
        # placeholder page to indicate form has been submitted.
        return render_template('404.html')
        # return redirect(url_for('main_route.results'))


@main_routes.route('/edit/<update>', methods=["POST"])
@login_required
def edit(update):

    return redirect(url_for('main_route.preference'))
# update value for the first name: first_name
# update value for the last name: last_name
# update value for the email: email
# update value for the location: city_id


@@main_routes.route('/followup', methods=['GET','POST'])
@login_required
def followup():
    return render_template('followup.html', firstName=current_user.first_name.capitalize())


