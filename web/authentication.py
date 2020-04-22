from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, City
from . import login_manager
from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer
from .utils import send_email

authentication = Blueprint("authentication",__name__)

# routes on user management
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@authentication.route('/sign_up', methods=['GET','POST'])
def sign_up():
    # when button to sign up on login page is clicked
    if request.method == 'GET':
        return render_template('signUp.html')
    elif request.method == 'POST':
        # check that email is not already registered
        email = str(request.form['email']).lower()
        user = db.session.query(User).filter(User.email==email).first()
        if not user:
            # Check that the user has indeed a Minerva e-mail
            if email.split("@")[1] == "minerva.kgi.edu":
                # create a new user profile
                # hash user password
                hashed_pwd = generate_password_hash(request.form['password'], method='sha256')
                # determine city
                city = db.session.query(City).filter(City.city_name==request.form.get('city_selected')).first()
                # add new user
                user = User(city_id=city.id, first_name=request.form['first_name'],last_name=request.form['last_name'], email=email,password=hashed_pwd, contact_method=request.form.get('contact_method'), contact_info=request.form['contact_info'])
                db.session.add(user)
                db.session.commit()

                # Login the user after signup
                logged_user = User.query.filter_by(email=email).first()
                login_user(logged_user, remember=False)
                return redirect(url_for('main_route.preference'))
            else:
                flash('Sorry, FoodBuddies is currently available only for Minerva students.',"inform")
                return render_template('signUp.html')
        else:
            flash('This email already has an account.',"error")
            return render_template('signUp.html')

# route will depend on whether how we structure pages
# is index the login + homepage or the page selecting preferences to then be matched?
@authentication.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = str(request.form['email']).lower()
        user = db.session.query(User).filter(User.email == email).first()
        # check that the user is in the database
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                # return redirect(url_for('index'))
                return redirect(url_for('main_route.preference'))
            else:
                flash('Incorrect Password!', "error")
                return redirect(url_for('authentication.login'))
        else:
            flash('This email does not have an account.', "error")
            return redirect(url_for('authentication.login'))

@authentication.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for(('main_route.index')))


@authentication.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    email = str(request.form['verEmail']).lower()
    user = db.session.query(User).filter(User.email == email).first()
    # check that the user is in the database
    if user:
        flash('An email sent to you for resetting your password!', 'inform')
        # Send the email with token
        send_password_reset_email(user.email)
        return redirect(url_for('authentication.login'))
    else:
        flash('This email does not have an account.', "error")
        return redirect(url_for('authentication.login'))

@authentication.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        # We try to decode the given token. Only tokens that are less than 3600 seconds old will be considered
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('authentication.login'))

    if request.method == 'POST':
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        # Find which user this email corresponds and updates the user password
        user.password = generate_password_hash(request.form['password'], method='sha256')
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('authentication.login'))
    else:
        return render_template('resetPassword.html', token=token)

def send_password_reset_email(user_email):
    # We will use the password_reset_serializer to create the token, which the user will receive through email.
    # The method creates a hash using SHA-512, to assure the user's safety.
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    password_reset_url = url_for('authentication.reset_with_token',token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'), _external=True)
    # We render the email design saved in the "email_password_reset" file
    html = render_template('email_password_reset.html', password_reset_url=password_reset_url)
    # Finally send the email
    send_email('Password Reset Requested', [user_email], html)
