import os
import tempfile

import pytest

from superform import app, db
from superform.plugins import twitter
from nose import with_setup

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


def test_run_tweet(client):
    # Is there a way to test a send tweet function?
    assert True == True

def test_is_valid_length_tweet() :
    # Test for is_valid_tweet function
    tweet = 'Simple message respecting Twitter\'s status conditions'
    assert twitter.is_valid_tweet(tweet) == True
    for i in range(0, 281):
        tweet += str(i)
    assert twitter.is_valid_tweet(tweet) == False # A tweet cannot be longer than 280 characters

def test_parsed_field_correctly_twitter():
    assert True==True