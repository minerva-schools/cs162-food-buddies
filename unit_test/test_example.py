# Example taken from:
# http://flask.pocoo.org/docs/1.0/testing/
# and suitably modified.
import os
import tempfile

import pytest

from web import app, db


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""
    # Changed the original test case bcs '/' redirects to the current login page
    rv = client.get('/')
    assert b'Login' in rv.data
