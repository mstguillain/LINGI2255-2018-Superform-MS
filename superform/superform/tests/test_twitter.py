import os
import tempfile
from datetime import datetime
#import twitter
#from ..superform import superform
#import importlib.utilspec= importlib.util.spec_from_file_location("")
from importlib import import_module
from flask import Blueprint, url_for, request, redirect, render_template, session


#from .superform.models import db, Publishing, Channel
#import pytest

from superform import app, db, Publishing, channels
from superform.models import Channel, db
from superform.plugins import twitter
from nose import with_setup
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


def test_run_tweet():
    pub = Publishing()
    pub.date_from='13.02.02'
    pub.title='test-Title'
    pub.description = 'descr'
    pub.image_url = 'imague url'
    pub.date_until = '14.02.16'
    pub.state = 1
    pub.channel_id='Twitter'

    c = db.session.query(Channel).first()

   # c = db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
    c_conf = c.config

    # credentials : if wrong internal error print the message ERRORRRRR
    status=twitter.run(pub, 'coucou')
    assert status =="uncorrect credentials"

    #publish empty tweet
    pub.description=''
   # status=twitter.run(pub, c_conf)
   # assert status==False


    #publish correct tweet

    pub.description=datetime.strftime(datetime.now(),"%Y-%m-%d-%h-%s-%m")
    status=twitter.run(pub,c_conf)
    assert status.text == pub.description




def test_is_valid_length_tweet() :
    # Test for is_valid_tweet function
    tweet = 'Simple message respecting Twitter\'s status conditions'
    assert twitter.is_valid_tweet(tweet) == True
    for i in range(0, 281):
        tweet += str(i)
    assert twitter.is_valid_tweet(tweet) == False # A tweet cannot be longer than 280 characters

