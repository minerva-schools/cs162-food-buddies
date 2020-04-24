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
        city = db.session.query(City).filter(City.id == current_user.city_id).first()
        return render_template('preference.html', user=current_user, city=city)
    elif request.method == 'POST':
        # check whether user preferences are already set
        app.logger.info("Post preference request")
        preference = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()
        if preference: # update preferences

            # determine linking to other tables
            cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name==request.form.get('cuisine_selected')).first()
            dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name==request.form.get('mealTime')).first()

            #update values
            preference.date_time = datetime.utcnow()
            if cuisine:
                preference.cuisine_id = cuisine.id
            preference.dinetime_id = dinetime.id
            preference.require_vegetarian = ("vegetarian" in request.form)
            preference.require_vegan = ("vegan" in request.form)
            preference.require_halal = ("halal" in request.form)
            preference.require_gluten_free = ("glutenFree" in request.form)
            preference.require_dairy_free = ("dairyFree" in request.form)
            preference.start_time = request.form['ava_from']
            preference.end_time = request.form['ava_to']
            #db.session.add(preference)
            db.session.commit()

        else: # set user preferences
            # determine linking to other tables
            cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name==request.form.get('cuisine_selected')).first()
            dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name==request.form.get('mealTime')).first()

            preference = Preference(date_time=datetime.utcnow(), user_id=current_user.id, cuisine_id=cuisine.id, dinetime_id=dinetime.id, city_id=current_user.city_id, require_vegetarian=("vegetarian" in request.form),require_vegan=("vegan" in request.form),require_halal=("halal" in request.form),require_gluten_free=("glutenFree" in request.form),require_dairy_free=("dairyFree" in request.form),start_time=request.form['ava_from'],end_time=request.form['ava_to'])
            db.session.add(preference)
            db.session.commit()
        # placeholder page to indicate form has been submitted.
        # return render_template('404.html')
        return redirect(url_for('main_route.loadMatches'))

@main_routes.route('/matches', methods=['GET','POST'])
@login_required
def loadMatches():
    # When user lands at the page, we load the matches based on the info stored at the DB
    if request.method == "GET":
        #Load the user preferences
        user_pref = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()

        # Try fo find perfect matches
        matchedUsers = db.session.query(User.first_name,User.last_name,Preference.require_vegetarian, Preference.require_vegan,\
                            Preference.require_dairy_free,Preference.require_halal,Preference.require_gluten_free,\
                            Cuisine.cuisine_name,DineTime.dinetime_name,User.contact_method,User.contact_info,User.email).\
                            join(Preference, Preference.user_id == User.id).join(DineTime, DineTime.id == Preference.dinetime_id).\
                            join(Cuisine, Cuisine.id == Preference.cuisine_id).join(City,Preference.city_id == City.id).\
                            filter(Preference.cuisine_id == user_pref.cuisine_id, Preference.dinetime_id == user_pref.dinetime_id,\
                            Preference.require_gluten_free == user_pref.require_gluten_free, Preference.require_halal == user_pref.require_halal,\
                            Preference.require_dairy_free == user_pref.require_dairy_free, Preference.require_vegan == user_pref.require_vegan,\
                            Preference.require_vegetarian == user_pref.require_vegetarian, Preference.city_id == current_user.city_id,\
                            User.id != current_user.id).all()

        # If none perfect matches were found, try matching ignoring dietary preferences
        if len(matchedUsers) == 0:
            matchedUsers = db.session.query(User.first_name, User.last_name, Preference.require_vegetarian,Preference.require_vegan, \
                        Preference.require_dairy_free, Preference.require_halal,Preference.require_gluten_free, \
                        Cuisine.cuisine_name, DineTime.dinetime_name, User.contact_method,User.contact_info, User.email). \
                        join(Preference, Preference.user_id == User.id).join(DineTime, DineTime.id == Preference.dinetime_id). \
                        join(Cuisine, Cuisine.id == Preference.cuisine_id).join(City,Preference.city_id == City.id). \
                        filter(Preference.cuisine_id == user_pref.cuisine_id, Preference.dinetime_id == user_pref.dinetime_id,\
                        Preference.city_id == current_user.city_id, User.id != current_user.id).all()

        # If none perfect matches were found above, try matching ignoring dietary preferences and cuisine
        if len(matchedUsers) == 0:
            matchedUsers = db.session.query(User.first_name, User.last_name, Preference.require_vegetarian,Preference.require_vegan, \
                                Preference.require_dairy_free, Preference.require_halal,Preference.require_gluten_free, \
                                Cuisine.cuisine_name, DineTime.dinetime_name, User.contact_method,User.contact_info, User.email). \
                                join(Preference, Preference.user_id == User.id).join(DineTime, DineTime.id == Preference.dinetime_id). \
                                join(Cuisine, Cuisine.id == Preference.cuisine_id).join(City,Preference.city_id == City.id). \
                                filter(Preference.dinetime_id == user_pref.dinetime_id, Preference.city_id == current_user.city_id,\
                                User.id != current_user.id).all()

        return render_template("matches.html", matchedUsers=matchedUsers)

    elif request.method == 'POST':
        # If the User updates their preferences on the page
        preference = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()
        cuisine = db.session.query(Cuisine).filter(Cuisine.cuisine_name == request.form.get('cuisine_selected')).first()
        dinetime = db.session.query(DineTime).filter(DineTime.dinetime_name == request.form.get('mealTime')).first()
        # update values
        preference.date_time = datetime.utcnow()
        if cuisine:
            preference.cuisine_id = cuisine.id
        preference.dinetime_id = dinetime.id
        preference.require_vegetarian = ("vegetarian" in request.form)
        preference.require_vegan = ("vegan" in request.form)
        preference.require_halal = ("halal" in request.form)
        preference.require_gluten_free = ("glutenFree" in request.form)
        preference.require_dairy_free = ("dairyFree" in request.form)
        db.session.add(preference)
        db.session.commit()

        return redirect(url_for('main_route.loadMatches'))

@main_routes.route('/edit/<update>', methods=["POST"])
@login_required
def edit(update):
    if update == "first_name":
        current_user.first_name = str(request.form.get("first_name")).capitalize()
    elif update == "last_name":
        current_user.last_name = str(request.form.get("last_name")).capitalize()
    elif update == "email":
        current_user.email = str(request.form.get("email")).lower()
    elif update == "contact_method":
        current_user.contact_method = request.form.get('contact_method')
        current_user.contact_info = request.form.get('contact_info')
    elif update == "city_name":
        city = db.session.query(City).filter(City.city_name==request.form.get('city_selected')).first()
        preference = db.session.query(Preference).filter(Preference.user_id == current_user.id).first()
        preference.city_id = city.id
        current_user.city_id = city.id
    db.session.commit()
    return redirect(url_for('main_route.preference'))