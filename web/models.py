from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum
from sqlalchemy.dialects.postgresql import ENUM
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
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    city = db.Column(ENUM(MinervaCities, create_type=False))
    #contact = db.Column(db.String(200))
