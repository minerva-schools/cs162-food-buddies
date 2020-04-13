import pytest
from web import create_app
import requests

@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config.from_object('web.config.TestingConfig')
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client  # this is where the testing happens!
    ctx.pop()

def test_home_page(client):
    resp = client.get('/login')
    assert b"Login" in resp.data
    assert resp.status_code == 200

def test_signup_page(client):
    resp = client.get('/sign_up')
    assert b"Sign up" in resp.data
    assert resp.status_code == 200

def test_non_existing_page(client):
    resp = client.get('/non_existing_page')
    assert resp.status_code == 404
