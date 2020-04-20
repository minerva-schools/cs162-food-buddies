from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#import enum
#from sqlalchemy.dialects.postgresql import ENUM

# create a db
db = SQLAlchemy()

# create table schema
class City(db.Model):
    '''Store current Minerva city names'''
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(80))

class User(db.Model, UserMixin):
    '''The User table store user name, city of residence, and contact info'''
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    #city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # each Minervan has a unique gmail address
    password = db.Column(db.String(200))
   # contact = db.Column(db.String(200)) # e.g. facebook account id
    city = db.Column(db.String(200), unique=False) # city name upon user selection

class Cuisine(db.Model):
    '''single-choice: cuisine options'''
    __tablename__ = 'Cuisine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cuisine_name = db.Column(db.String(100))

class DineTime(db.Model):
    '''single-choice: dining time of the day'''
    __tablename__ = 'DineTime'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dinetime_name = db.Column(db.String(100))

class Preference(db.Model):
    '''Time-stamped log of user preference, each row is updated upon user refresh of the 'results' page
    * columns starting with 'require_' record user's latest dietary restrictions (multi-selectable), default False
    * 'matched' column is updated to True if the user has found a match
    '''
    __tablename__ = 'Preference'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('Cuisine.id'))
    dinetime_id = db.Column(db.Integer, db.ForeignKey('DineTime.id'))
    # multi-selection of food restrictions
    require_vegetarian = db.Column(db.Boolean, default=False )
    require_vegan = db.Column(db.Boolean, default=False)
    require_halal = db.Column(db.Boolean, default=False)
    require_gluten_free = db.Column(db.Boolean,default=False )
    require_dairy_free = db.Column(db.Boolean,default=False )

    matched = db.Column(db.Boolean, default=False) # True if a buddy is found
