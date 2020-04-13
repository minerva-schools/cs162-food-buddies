import pytest
from web import create_app, db
import requests

@pytest.fixture
def app():
    app = create_app('test')
    app.config.from_object('web.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    return app

def test_valid_sign_up(app):
    # After sign-up, the User should see the Preferences page
    client = app.test_client()
    resp = client.post('/sign_up',data=dict(email="testemail@gmail.com", first_name="Test", last_name="User",
                                            password="passsword123"), follow_redirects=True)
    assert b"Preferences" in resp.data
    assert resp.status_code == 200

def test_invalid_sign_up(app):
    client = app.test_client()
    resp = client.post('/sign_up', data=dict(email="testemail@gmail.com", first_name="Test", last_name="User",
                                             password="passsword123"), follow_redirects=True)
    assert resp.status_code == 200
    resp = client.post('/sign_up', data=dict(email="testemail@gmail.com", first_name="Test 2", last_name="New User 2",
                                             password="passsword456"), follow_redirects=True)
    assert b"This email already has an account." in resp.data

def test_invalid_login(app):
    client = app.test_client()
    resp = client.post('/login', data=dict(email="testemail@gmail.com", password="passsword123"), follow_redirects=True)
    assert b"This email does not have an account" in resp.data

def test_invalid_password(app):
    client = app.test_client()
    # Create an account
    resp = client.post('/sign_up', data=dict(email="testemail@gmail.com", first_name="Test", last_name="User",
                                             password="passsword123"), follow_redirects=True)
    assert resp.status_code == 200
    # Try to login with the wrong password
    resp = client.post('/login', data=dict(email="testemail@gmail.com", password="passsword456"), follow_redirects=True)
    assert b"Incorrect Password!" in resp.data


