import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from web.models import User, Preference, City
import time

@pytest.fixture
def Session():
    db_uri = "sqlite:///web/test.db"
    engine = create_engine(db_uri, echo=True)
    Base = declarative_base(engine)
    Session = sessionmaker(bind=engine)
    return Session


def test_change_name(Session):
    testSession = Session()
    with requests.Session() as s:
        # SignUp a new User
        resp = s.post('http://127.0.0.1:5000/sign_up',data=dict(email="harry.potter@minerva.kgi.edu", first_name="Harry", last_name="Potter",password="passsword123",
            contact_method='Phone', contact_info='+1 415-123-4567', city_selected='San Francisco'),allow_redirects=True)
        assert resp.status_code == 200

        # The User should be in the database
        u = testSession.query(User).filter(User.email=="harry.potter@minerva.kgi.edu").first()
        assert u.first_name == "Harry"
        assert u.last_name == "Potter"

        # Let's change the user name
        resp = s.post('http://127.0.0.1:5000/edit/first_name',data=dict(first_name="Tony"),allow_redirects=True)
        assert resp.status_code == 200
        assert "Hi Tony" in resp.text

        resp = s.post('http://127.0.0.1:5000/edit/last_name', data=dict(last_name="Stark"), allow_redirects=True)
        assert resp.status_code == 200
        assert "Stark" in resp.text

        # For some reason, when I update an object, I need to reconnect the session, otherwise it won't propagate the
        # updates
        testSession.close()
        testSession = Session()

        u = testSession.query(User).filter(User.email == "harry.potter@minerva.kgi.edu").first()
        assert u.first_name == "Tony"
        assert u.last_name == "Stark"

        # Log-out with this User
        r = s.get('http://127.0.0.1:5000/logout')
        assert "Login" in r.text

        testSession.close()

def test_user_email(Session):
    testSession = Session()
    with requests.Session() as s:
        resp = s.post('http://127.0.0.1:5000/login',data=dict(email="harry.potter@minerva.kgi.edu",password="passsword123"))
        assert resp.status_code == 200
        assert "Preferences" in resp.text

        resp = s.post('http://127.0.0.1:5000/edit/last_name', data=dict(last_name="Stark"), allow_redirects=True)
        resp = s.post('http://127.0.0.1:5000/edit/email', data=dict(email="tony.stark@minerva.kgi.edu"), allow_redirects=True)
        assert resp.status_code == 200

        # Check that are no more users registered under "harry.potter@minerva.kgi.edu"
        u = testSession.query(User).filter(User.email == "harry.potter@minerva.kgi.edu").first()
        assert u == None

        # Log-out with this User
        r = s.get('http://127.0.0.1:5000/logout')
        assert "Login" in r.text

        # Log in using the new email
        resp = s.post('http://127.0.0.1:5000/login', data=dict(email="tony.stark@minerva.kgi.edu", password="passsword123"))
        assert resp.status_code == 200
        assert "Preferences" in resp.text

        testSession.close()
        testSession = Session()

        u = testSession.query(User).filter(User.email == "tony.stark@minerva.kgi.edu").first()
        assert u.first_name == "Tony"
        assert u.last_name == "Stark"

        testSession.close()

def test_edit_duplicate_email():
    with requests.Session() as s:
        # Log in using the test user
        resp = s.post('http://127.0.0.1:5000/login', data=dict(email="tony.stark@minerva.kgi.edu", password="passsword123"))
        assert resp.status_code == 200
        assert "Preferences" in resp.text

        # Try to change the email addr to one that is already been used by one of the dummy users.
        resp = s.post('http://127.0.0.1:5000/edit/email',data=dict(email="david.mitchell@minerva.kgi.edu"))
        assert "An account using this email already exists" in resp.text

def test_edit_non_minerva_email():
    with requests.Session() as s:
        # Log in using the test email
        resp = s.post('http://127.0.0.1:5000/login', data=dict(email="tony.stark@minerva.kgi.edu", password="passsword123"))
        assert resp.status_code == 200
        assert "Preferences" in resp.text

        # Try to change the email to a non-Minerva domain
        resp = s.post('http://127.0.0.1:5000/edit/email',data=dict(email="tony@stakenterprises.com"))
        assert "Unfortunately, we can only offer support to Minerva users" in resp.text

def test_edit_contact_information(Session):
    with requests.Session() as s:
        testSession = Session()
        # Log in using the test email
        resp = s.post('http://127.0.0.1:5000/login', data=dict(email="tony.stark@minerva.kgi.edu", password="passsword123"))
        assert resp.status_code == 200
        assert "Preferences" in resp.text

        u = testSession.query(User).filter(User.email == "tony.stark@minerva.kgi.edu").first()
        assert u.contact_method == "Phone"
        assert u.contact_info == "+1 415-123-4567"
        testSession.close()

        resp = s.post('http://127.0.0.1:5000/edit/contact_method', data=dict(contact_method="WhatsApp", contact_info="+1 628-987-5432"))
        assert resp.status_code == 200

        testSession = Session()
        u = testSession.query(User).filter(User.email == "tony.stark@minerva.kgi.edu").first()
        assert u.contact_method == "WhatsApp"
        assert u.contact_info == "+1 628-987-5432"

        # Lastly, let's delete the test user
        testSession.delete(u)
        testSession.commit()
        testSession.close()

