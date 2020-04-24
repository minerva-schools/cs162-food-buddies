from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import Blueprint
from flask import current_app as app
from datetime import datetime
from .models import db, User, City, Cuisine, Preference, DineTime

# to save uploaded images to folder
import os
import random

# create an app factory
main_routes = Blueprint('main_route',__name__,template_folder='templates')

# placeholder reference to homepage
@main_routes.route('/')
def index():
    return render_template('login.html')


def get_img_path():
    '''helper function to get the path to user profile image'''
    if current_user.profile_img_name: # if there is a user-uploaded image
        image_name = current_user.profile_img_name # strings in db
    else:
        image_name = "profilePicPlaceholder.png"
    # construct image path to user profile photo
    image_path = os.path.join(app.root_path, 'static/userProfilePics',image_name)
    return image_path


@main_routes.route('/preference', methods=['GET','POST'])
@login_required
def preference():
    if request.method == 'GET' :
        return render_template('preference.html',
            firstName=current_user.first_name.capitalize(),
            lastName=current_user.last_name.capitalize(),
            email=current_user.email,
            contactInfo=current_user.contact_info,
            imagePath=get_img_path()
           )
        
    elif request.method == 'POST' :

        # if a profile photo is uploaded through a POST method before
        if request.form.get('new_img'):
            file = request.files['new_img'] # the File object (from Flask request)
            srcfile_name = file.filename.lower()
            ext = os.path.splitext(srcfile_name)[-1].lower() # get the extension
            # delete any old file
            if current_user.profile_img_name!=None:
                os.remove(os.path.join(app.root_path, 'static/userProfilePics',current_user.profile_img_name))
                # name the new profile
            filename_db = 'user_'+str(current_user.id)+'_'+str(random.randint(1000,9999))+ext # the
            # save this new file to user upload folder
            file.save(os.path.join(app.root_path, 'static/userProfilePics',filename_db))
            # update corresponding file_name in db upon first upload
            db.session.query(User).filter(User.id==current_user.id).update({'profile_img_name': filename_db})
            db.session.commit() # commit any changes
            
            return redirect(url_for('main_route.preference'))

        # else, the POST cnocerns preference updates
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

    if request.form.get('new_img'):
        return redirect(url_for('main_route.preference'))
    
    else:
        new_first_name = request.form.get('new_first_name')
        if new_first_name:
            db.session.query(User).filter(User.id==current_user.id).update({'first_name': new_first_name})
            db.session.commit() # commit any changes
            
        new_last_name = request.form.get('new_last_name')
        if new_last_name:
            db.session.query(User).filter(User.id==current_user.id).update({'last_name': new_last_name})
            db.session.commit() # commit any changes
                   
        new_email =request.form.get('new_email')
        if new_email:
            db.session.query(User).filter(User.id==current_user.id).update({'email': new_email})
            db.session.commit() # commit any changes

        db.session.query(User).filter(User.id==current_user.id).update({'city_id': new_city_id})
        new_city_name =request.form.get('new_city_name')
        if new_city_name:
                # retrieve city_id
            results = db.session.query(City.id).filter(City.city_name==new_city_name)
            for r in results:
                new_city_id = r[0]
            db.session.query(User).filter(User.id==current_user.id).update({'city_id': new_city_id})
            db.session.commit() # commit any changes
            
        new_contact_method =request.form.get('new_contact_method')
        if new_contact_method:
            db.session.query(User).filter(User.id==current_user.id).update({'contact_method': new_contact_method})
            db.session.commit() # commit any changes

        new_contact_info=request.form.get('new_contact_info')
        if new_contact_info:
            db.session.query(User).filter(User.id==current_user.id).update({'contact_info': new_contact_info})
            db.session.commit() # commit any changes
            
        return redirect(url_for('main_route.preference'))

