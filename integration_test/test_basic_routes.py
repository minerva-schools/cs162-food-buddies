import requests

def test_basic_request():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

def test_signup_request():
    r = requests.get('http://127.0.0.1:5000/sign_up')
    assert r.status_code == 200

def test_404_error_handler():
    r = requests.get('http://127.0.0.1:5000/this_page_is_fake')
    assert r.status_code == 404
    assert "Either you requested invalid page or you don't have permission to access this page." in r.text

def test_redirect_preferences():
    r = requests.get('http://127.0.0.1:5000/preference')
    assert r.status_code == 200
    assert 'You need to login for accessing this page!' in r.text

def test_redirect_matches():
    r = requests.get('http://127.0.0.1:5000/matches')
    assert r.status_code == 200
    assert 'You need to login for accessing this page!' in r.text

# def test_redirect_followup():
#     r = client.get('http://127.0.0.1:5000/followup')
#     assert r.status_code == 200
#     assert b'You need to login for accessing this page!' in r.text
