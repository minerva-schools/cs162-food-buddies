import os
import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from web.models import User, Preference, City
import time

@pytest.fixture
def testSession():
    db_uri = "sqlite:///web/test.db"
    engine = create_engine(db_uri, echo=True)
    Base = declarative_base(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_valid_user_flow(testSession):
    ''' We create a new user, located in San Francisco, and check whether the buddies indicates by the app are
    those expected given the dummy users created and the preferences inserted for the current user '''


    with requests.Session() as s:
        # SignUp a new User
        resp = s.post('http://127.0.0.1:5000/sign_up',data=dict(email="testintegration@minerva.kgi.edu", first_name="Test", last_name="User",password="passsword123",
            contact_method='Phone', contact_info='88888888', city_selected='San Francisco'),allow_redirects=True)
        assert resp.status_code == 200

        # The User should be in the database
        u = testSession.query(User).filter(User.email=="testintegration@minerva.kgi.edu").first()
        assert u.first_name == "Test"
        assert u.last_name == "User"

        # set user preferences
        r = s.post('http://127.0.0.1:5000/preference', data=dict(vegan=True,
            mealTime='Lunch', cuisine_selected="American", ava_from="12:30", ava_to="14:00"), allow_redirects=True)
        assert r.status_code == 200

        # These preferences should be in the DB
        pref = testSession.query(Preference).filter(Preference.user_id == u.id).first()
        assert pref.require_vegan == True
        assert pref.require_vegetarian == False
        assert pref.start_time == "12:30"
        assert pref.end_time == "14:00"

        # check perfect matches returned --
        assert "James" in r.text
        assert "Kia" in r.text
        assert "Bea" in r.text
        assert "Charles" not in r.text
        assert "nomatching.png" not in r.text

        # edit user preferences, on the matches page
        r = s.post('http://127.0.0.1:5000/matches', data=dict(vegetarian=True,
            mealTime='Dinner', cuisine_selected="European"), allow_redirects=True)
        assert r.status_code == 200

        # check no matches now, because no dummy users are looking for buddies for dinner
        assert "James" not in r.text
        assert "Kia" not in r.text
        assert "Bea" not in r.text
        assert "Charles" not in r.text
        assert "nomatching.png" in r.text

        # Log-out with this User
        r = s.get('http://127.0.0.1:5000/logout')
        assert "Login" in r.text

def test_returning_user_flow(testSession):
    with requests.Session() as s:
        u = testSession.query(User).filter(User.email == "testintegration@minerva.kgi.edu").first()

        # Log-in with the user create before
        r = s.post('http://127.0.0.1:5000/login', data=dict(email="testintegration@minerva.kgi.edu", password="passsword123"))
        assert r.status_code == 200
        assert "Preferences" in r.text

        # The previous preferences updated should be in the DB
        pref = testSession.query(Preference).filter(Preference.user_id == u.id).first()
        assert pref.require_vegetarian == True
        assert pref.require_vegan == False

        # Update the user preferences
        r = s.post('http://127.0.0.1:5000/preference', data=dict(vegan=True,mealTime='Lunch', cuisine_selected="Latin American",
             ava_from="12:30", ava_to="14:00"), allow_redirects=True)
        assert r.status_code == 200

        # Charles is the only match for Lunch AND Latin American cuisine
        assert "James" not in r.text
        assert "Kia" not in r.text
        assert "Bea" not in r.text
        assert "Charles" in r.text

        # log out with that user
        r = s.get('http://127.0.0.1:5000/logout')
        assert "Login" in r.text

def test_changed_city(testSession):
    with requests.Session() as s:
        u = testSession.query(User).filter(User.email == "testintegration@minerva.kgi.edu").first()

        # Log-in with the user create before
        r = s.post('http://127.0.0.1:5000/login', data=dict(email="testintegration@minerva.kgi.edu", password="passsword123"))
        assert r.status_code == 200
        assert "Preferences" in r.text

        # Our User has moved and it is now in Seoul
        r = s.post('http://127.0.0.1:5000/edit/city_name',data=dict(city_selected='Seoul'))
        assert r.status_code == 200


        # Updated user preferences for Vegan + Lunch + European
        r = s.post('http://127.0.0.1:5000/preference', data=dict(vegan=True, mealTime='Lunch', cuisine_selected="European",
                             ava_from="12:30", ava_to="14:00"), allow_redirects=True)
        assert r.status_code == 200

        # David is the only match for Lunch + European
        assert "Jingren" not in r.text
        assert "David" in r.text
        assert "Stephen" not in r.text

        # Updated user preferences for Lunch + Vegetarian + American
        r = s.post('http://127.0.0.1:5000/matches', data=dict(vegetarian=True, mealTime='Lunch', cuisine_selected="American"),
                   allow_redirects=True)
        assert r.status_code == 200

        # All users should show-up, but none is a perfect match. They only share interest for "Lunch"
        assert "Jingren" in r.text
        assert "David" in r.text
        assert "Stephen" in r.text

        # log out with that user
        r = s.get('http://127.0.0.1:5000/logout')
        assert "Login" in r.text

    # Remove the user from the DB
    testSession.delete(u)
    testSession.commit()
