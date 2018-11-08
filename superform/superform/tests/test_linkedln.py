import datetime
import os
import tempfile
import traceback
import pytest
from linkedin import linkedin
import json

from superform import app, db, Publishing, channels
from superform.plugins import LinkedIn
from superform.models import Channel, db


## pip install python-linkedin
## log in : tip.hon2014@gmail.com
## pwd : PwdForTeam06



def test_run_linkedin():
    """
    Checks if a simple linkindin post can be created (require a session bein present in the db
    :return:
    """
    pub = Publishing()
    pub.date_from='13.02.02'
    pub.title='test-Title'
    pub.link_url = 'a link'
    pub.description = 'descr'
    pub.image_url = 'image url'
    pub.date_until = '14.02.19'
    pub.state = 1
    print("le test run linkedin est launched")
    linkedIn_Channel = db.session.query(Channel).filter(Channel.module == "superform.plugins.LinkedIn").first()
    if(linkedIn_Channel is None):
        print("LinkedIn test failed since the db contains no LinkedIn channel") #TODO pytest test_ignore ?
    else:
        channel_config=linkedIn_Channel.config
        json_data = json.loads(channel_config)
        pub.channel_id = json_data['id']
        status = linkedin.run(pub, channel_config)
        assert status == "Post successful"