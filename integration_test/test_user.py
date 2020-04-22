import os
import pytest
import requests
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from web.models import User

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

    # log out with that user
    r = requests.get('http://127.0.0.1:5000/logout')
    assert "Login" in r.text

    # Now log-in with the same User
    r = requests.post('http://127.0.0.1:5000/login',data=dict(email="testemail@gmail.com", password="passsword123"))
    assert r.status_code == 200
    assert "Preferences" in r.text

    # log out with that user
    r = requests.get('http://127.0.0.1:5000/logout')
    assert "Login" in r.text

    # Remove the user from the DB
    testSession.delete(u)
    testSession.commit()



