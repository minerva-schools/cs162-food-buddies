from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from flask import current_app as app
from flask import Blueprint

main_routes = Blueprint('main_route',__name__)

# placeholder reference to homepage
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/preference', methods=['GET','POST'])
@login_required
def preference():
    return render_template('preference.html', firstName=current_user.first_name.capitalize())
    #For getting the location of use the following line
    # request.form.get ("location")
    #For getting the mealTime use the following line 
    #request.form.get ("mealTime")
    #For getting the dietary preferences use the following line
    #request.form.getlist ("dietary")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def custom_401(e):
    flash('You need to login for accessing this page!')
    return redirect(url_for('authentication.login'))

