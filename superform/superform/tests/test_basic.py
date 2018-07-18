#To run : Be sure to be in Superform/superform folder and then 'pytest -v' in your terminal

import os
import tempfile

import pytest

from superform import app, db


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_index(client):
    rv = client.get('/',follow_redirects=True)
    assert rv.status_code == 200
    assert "Your are not logged in." in rv.data.decode()
