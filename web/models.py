from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# create a db
db = SQLAlchemy()

# create table schema

class City(db.Model):
    '''Store current Minerva city names'''
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(80))

class User(db.Model, UserMixin):
    '''The User table store user name, city of residence, and contact info.
        * City_id as foreign key for buddy filtering'''
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # each Minervan has a unique gmail address
    password = db.Column(db.String(200))
    contact_method = db.Column(db.String(100))
    contact_info = db.Column(db.String(300))
    profile_img_name = db.Column(db.String(100), nullable=True)


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
    #date_time = db.Column(db.DateTime)
    date_time=db.Column(db.String(100))

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

    # time availability
    # store start/end time of desired dining time as integer (0 - 24th hour of the day)
    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))
    
    matched = db.Column(db.Boolean, default=False) # True if a buddy is found



# define event listeners
# * each lister inserts default data to the specified table (only once) after db creation
@db.event.listens_for(City.__table__, 'after_create', once=True)
def insert_city_options(*args, **kwargs):
    '''insert Minerva city options upon db creation'''
    MinervaCities = ['San Francisco', 'Seoul', 'Hyderabad', 'Berlin', 'Buenos Aires', 'London', 'Taipei']
    for city_name in MinervaCities:
        db.session.add(City(city_name=city_name))
    db.session.commit()
        
@db.event.listens_for(Cuisine.__table__, 'after_create', once=True)
def insert_cuisine_options(*args, **kwargs):
    '''insert cuisine options upon db creation'''
    CuisineTypes = ['American', 'Asian', 'European', 'Middle Eastern', 'Latin American', 'Subcontinental']
    for cuisine_name in CuisineTypes:
        db.session.add(Cuisine(cuisine_name=cuisine_name))
    db.session.commit()

@db.event.listens_for(DineTime.__table__, 'after_create', once=True)
def insert_dinetime_options(*args, **kwargs):
    '''insert dining time options upon db creation'''
    DiningTimes = ['Lunch', 'Dinner', 'Breakfast']
    for dinetime_name in DiningTimes:
        db.session.add(DineTime(dinetime_name=dinetime_name))
    db.session.commit()
        
               
# dump in some dummy user data upon db creation (for demo purpose)
@db.event.listens_for(User.__table__, 'after_create', once=True)
def insert_dummy_users(*args, **kwargs):
    '''insert dummy user data upon db creation'''
    # hashed password strings
    hashedPW = {   # keys are the actual passwords from dummy user input (please use them to login)
        88888888: 'sha256$30buaXI6$085be32da5b90c6b3bb002e7ba4764c1f4f4fa070b7d263c870a621e55efe2ee',
        77777777: 'sha256$ZLmXsoHR$cbd1ea13546619e8291686f46822c77a7e8099e5e7bc0095b1329a81f821fe8a',
        66666666: 'sha256$7nZiviKc$21edefd8abe3f32baa7284a24a90dab793b5c94cf7a63cec5e1fb283d1160f3d',
        55555555: 'sha256$V7vmFKKC$d2a91f308dc90375cf5b07021c5830cd593146ead60f757bc607c6cbfec6e4b2'
        }
        
    DummyUsers = [
            [2,'Jingren', 'Wang', 'jingren.wang@minerva.kgi.edu',
        hashedPW[88888888], 'Phone', '+82 105-557-7494', 'user_1.jpeg'], # Seoul
            [5,'Mary', 'Burns', 'mary.burns@minerva.kgi.edu',
        hashedPW[77777777], 'Phone', '+54 155-5516-605', 'user_2.jpg'], # Buenos Aires
            [1,'James', 'Gordon', 'james.gordon@minerva.kgi.edu',
        hashedPW[66666666], 'Phone', '+1 729-591-1038',None ], # San Francisco
            [1,'Kia', 'Louis', 'kia.louis@minerva.kgi.edu',
        hashedPW[55555555], 'Phone', '+1 813-028-4012', None] # San Francisco
        ]

    for user_info in DummyUsers:
        if user_info[7]:
            user_img_name = str(user_info[7])
        else:
            user_img_name = 'profilePicPlaceholder.png'
            
        db.session.add(User( city_id=user_info[0],
            first_name=user_info[1], last_name=user_info[2],
                email=user_info[3], password=user_info[4],
                contact_method=user_info[5], contact_info=user_info[6],
                profile_img_name = user_info[7]))
    db.session.commit()
        

# dump in some dummy preferences upon db creation
@db.event.listens_for(Preference.__table__, 'after_create', once=True)
def insert_dummy_preferences(*args, **kwargs):
    '''insert one dummy user preference upon db creation'''
    db.session.add(Preference(
        date_time='2020-05-01 11:05:26',
            user_id=2, city_id=5, cuisine_id=3, dinetime_id=1,
            require_vegan=True, start_time='11:10:00', end_time='13:30:00'
            ))
            # *other 'require_' attributes default to Flase (0)
    db.session.commit()
