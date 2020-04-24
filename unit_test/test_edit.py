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

def test_change_Fname(client):
    resp = client.post('/edit/first_name', data=dict(first_name="Mark"), follow_redirects=True)
    assert resp.status_code == 200

def test_change_Lname(client):
    resp = client.post('/edit/last_name', data=dict(last_name="Ben"), follow_redirects=True)
    assert resp.status_code == 200

def test_change_vaild_email(client):
    resp = client.post('/edit/email', data=dict(last_name="test_change@minerva.kgi.edu"), follow_redirects=True)
    assert resp.status_code == 200

def test_change_location(client):
    resp = client.post('/edit/city_name', data=dict(city_name="San Francisco"), follow_redirects=True)
    assert resp.status_code == 200

def test_change_contact_method(client):
    resp = client.post('/edit/contact_method', data=dict(contact_method="Phone",contact_info="01200196366" ), follow_redirects=True)
    assert resp.status_code == 200
