import os
import sys
import tempfile
from datetime import datetime
import string
import random
from twitter import twitter_utils

#import pytest

from superform import app, db, Publishing, channels
from superform.models import Channel, db
from superform.plugins import twitter



def test_run_tweet():
    pub = Publishing()
    pub.date_from='13.02.02'
    pub.title='test-Title'
    pub.link_url = 'blablablablablablablajdsfvjdbvjdnfvqebdnbqdfnvsdùnvbmqknkfnbùsfvdf'
    pub.description = 'descr'
    pub.image_url = 'imague url'
    pub.date_until = '14.02.16'
    pub.state = 1
    pub.channel_id='Twitter'

    #c = db.session.query(Channel).first()
    #c_conf = c.config

    # credentials : if wrong internal error print the message
    status=twitter.run(pub, 'coucou')
    assert status =="uncorrect credentials"

    #publish empty tweet
    pub.description=''
    #status=twitter.run(pub, c_conf)
    #assert status==False


    #publish correct tweet

    pub.description=datetime.strftime(datetime.now(),"%Y-%m-%d-%h-%s-%m")
    #status=twitter.run(pub,c_conf)
    #assert status.text == pub.description

    #publish correct tweet over 280 character
    pub.description=datetime.strftime(datetime.now(),"%Y-%m-%d-%h-%s-%m")+" jpjpswjfdkjm pjwdfvkj<dfvw j<hgiuwdh wjdfvjdf wjhvfifdh jkxfbgkjwnf jxfbjxfjb jxdjfnbjfd lkxgfb wdjf kcnji hv yxbyxdyv bb jxdf gjb x:khvsjhvish beatae dolorem rerum.Aspernatur eos iure facilis vero dolore nemo sint. Velit qui nobis necessitatibus provident repudiandae iure excepturi. Ad odit necessitatibus accusamus ut hic ut sunt. Delectus qui error unde eius occaecati."
   # pub.description=str(pub.description)

    #status = twitter.run(pub, c_conf)

    assert status != False
    #assert status != "uncorrect credentials"



def test_is_valid_length_tweet() :
    # Test for is_valid_tweet function
    tweet = 'Simple message respecting Twitter\'s status conditions'
    assert twitter.tweet_too_big(tweet) == False
    for i in range(0, 281):
        tweet += str(i)
    assert twitter.tweet_too_big(tweet) == True # A tweet cannot be longer than 280 characters
