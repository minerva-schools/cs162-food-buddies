import requests
import pytest
import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper
#from sqlalchemy.ext.declarative import declarative_base
#from web.models import User


@pytest.fixture
def testSession():
    db_uri = "sqlite:///web/test.db"
    engine = create_engine(db_uri)
    # Base = declarative_base(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    # data = session.query(User).all()
    yield session
    session.close()


def test_basic_request():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

def test_db(testSession):
    pass
    #testSession.add(User(first_name="First Name", last_name="Last name", email="lucas@gmail.com", password="My password"))
    #testSession.commit()
    #data = testSession.query(User).first()
    #assert data.first_name == "First Name"
