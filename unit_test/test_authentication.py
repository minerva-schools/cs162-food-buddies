import pytest

from web import create_app, db
from web.models import User
import os
import requests

@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    app.config.from_object('web.config.TestingConfig')
    with app.app_context():
        # Initialize the db tables
        db.create_all()
        yield app
        # Remove only the users crated here. Dummy users will be left intact
        User.query.filter(User.email == "testemail@minerva.kgi.edu").delete()

    return app

def test_valid_sign_up(app):
    # After sign-up, the User should see the Preferences page
    client = app.test_client()
    resp = client.post('/sign_up',data=dict(
            email="testemail@minerva.kgi.edu",
            first_name="Test", last_name="User",
            password="passsword123",
            contact_method='Phone', contact_info='88888888', city_selected='San Francisco'), follow_redirects=True)
            
    assert b"Preferences" in resp.data
    assert resp.status_code == 200

def test_invalid_sign_up(app):
    # Attempt to sign-up with a duplicate email
    client = app.test_client()

    resp = client.post('/sign_up', data=dict(email="mary.burns@minerva.kgi.edu", first_name="Test 2", last_name="New User 2",
                                             password="passsword456"), follow_redirects=True)
    assert b"This email already has an account." in resp.data

def test_invalid_login(app):
    # Attempt to sign-in with a non-existing account
    client = app.test_client()
    resp = client.post('/login', data=dict(email="notestemail@minerva.kgi.edu", password="passsword123"), follow_redirects=True)
    assert b"This email does not have an account" in resp.data

def test_invalid_password(app):
    # Attempt to sign-in with the wrong password
    client = app.test_client()

    # Try to login with the wrong password
    resp = client.post('/login', data=dict(email="mary.burns@minerva.kgi.edu", password="wrong_pwd"), follow_redirects=True)
    assert b"Incorrect Password!" in resp.data

def test_valid_login(app):
    # After logging-in the User should see the preferences page
    client = app.test_client()

    #Login with that account
    resp = client.post('/login', data=dict(email="james.gorden@minerva.kgi.edu", password="66666666"), follow_redirects=True)
    assert resp.status_code == 200
    assert b"Preferences" in resp.data

def test_logout(app):
    # After logging-in the User should see the preferences page
    client = app.test_client()

    #Login with that account
    resp = client.post('/login', data=dict(email="kia.louis@minerva.kgi.edu", password="55555555"), follow_redirects=True)
    assert resp.status_code == 200
    assert b"Preferences" in resp.data

    resp = client.get('/logout',follow_redirects=True)
    assert resp.status_code == 200
    assert b"Login" in resp.data

def test_non_minervan_sign_up(app):
    client = app.test_client()

    resp = client.post('/sign_up', data=dict(
        email="testemail@gmail.com",
        first_name="Test", last_name="User",
        password="passsword123",
        contact_method='Phone', contact_info='88888888', city_selected='San Francisco'), follow_redirects=True)

    assert b"Sorry, FoodBuddies is currently available only for Minerva students." in resp.data