from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum
db = SQLAlchemy()

class MinervaCities(enum.Enum):
    SanFrancisco = 'San Francisco'
    Seoul = 'Seoul'
    Hyderabad = 'Hyderabad'
    Berlin = 'Berlin'
    BuenosAires = 'Buenos Aires'
    London = 'London'
    Taipei = 'Taipei'


class User(db.Model,UserMixin):
    '''The User table store user name, city of residence, and contact info'''
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # each Minervan has a unique gmail address
    password = db.Column(db.String(200))
    city = db.Column(db.Enum(MinervaCities))
    # contact ?? can add facebook accounts


