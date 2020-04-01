from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from .models import db
from .authentication import authentication, login_manager

app = Flask(__name__)

app.register_blueprint(authentication, url_prefix="/")
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db.init_app(app)
with app.test_request_context():
    db.create_all()

login_manager.init_app(app)

# placeholder reference to homepage
@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()




