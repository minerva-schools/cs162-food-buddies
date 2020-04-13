import pytest
from web import create_app, db
import flask

@pytest.fixture
def app():
    app = create_app('test')
    app.config.from_object('web.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    return app

def test_home_page(app):
    client = app.test_client()
    resp = client.get('/')
    assert b"Login" in resp.data
    assert resp.status_code == 200

def test_signup_page(app):
    client = app.test_client()
    resp = client.get('/sign_up')
    assert b"Sign up" in resp.data
    assert resp.status_code == 200