import os
import pytest
import requests
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from web.models import User, Preference

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
    # SignUp a new User
    r = requests.post('http://127.0.0.1:5000/sign_up',data=dict(email="testemail@minerva.kgi.edu", first_name="Test", last_name="User",password="passsword123",
        contact_method='Phone', contact_info='88888888', city_selected='San Francisco'),allow_redirects=True)
    assert r.status_code == 200

    # The User should be in the database
    u = testSession.query(User).filter(User.email=="testemail@minerva.kgi.edu").first()
    assert u.first_name == "Test"
    assert u.last_name == "User"

    # set user preferences
    r = requests.post('http://127.0.0.1:5000/preference', data=dict(vegan=True,
        mealTime='Lunch', cuisine_selected="American", ava_from="12:30", ava_to="14:00"), allow_redirects=True)
    assert r.status_code == 200

    # preference should be in the database
    p = testSession.query(Preference).filter(Preference.require_vegan==True).last()
    assert p.start_time == "12:30"
    assert p.end_time == "14:00"

    # check perfect matches returned -- are we limiting results?
    r = requests.get('http://127.0.0.1:5000/matches')
    assert "James" in r.text
    assert "Kia" in r.text
    assert "Bea" in r.text
    assert "Charles" in r.text

    # edit user preferences
    r = requests.post('http://127.0.0.1:5000/preference', data=dict(vegetarian=True,
        mealTime='Dinner', cuisine_selected="European", ava_from="11:30", ava_to="13:30"), allow_redirects=True)
    assert r.status_code == 200

    # preference should be in the database
    p = testSession.query(Preference).filter(Preference.require_vegaetarian==True).last()
    assert p.start_time == "11:30"
    assert p.end_time == "13:30"

    # check no matches now
    r = requests.get('http://127.0.0.1:5000/matches')
    assert "James" not in r.text
    assert "Kia" not in r.text
    assert "Bea" not in r.text
    assert "Charles" not in r.text

    # change preferences on matches page


    # check matches using non-perfect query


    # log out with that user
    r = requests.get('http://127.0.0.1:5000/logout')
    assert "Login" in r.text

    # Now log-in with the same User
    r = requests.post('http://127.0.0.1:5000/login',data=dict(email="testemail@minerva.kgi.edu", password="passsword123"))
    assert r.status_code == 200
    assert "Preferences" in r.text

    # log out with that user
    r = requests.get('http://127.0.0.1:5000/logout')
    assert "Login" in r.text

    # Remove the user from the DB
    testSession.delete(u)
    testSession.commit()
