import sys
sys.path.append("..")
#Gcal import
from datetime import datetime
from plugins.gcal_plugin import *
from publishings import *
from models import *
from googleapiclient.discovery import build
#facebook import
from plugins.facebook_plugin import *
import unittest
from urllib.request import urlopen
#Stats import
import stats

#We look first the number of post and then we publish a post and then we relook if the number of post is +1
def test_GCAL_post():

    k = stats.number_of_posts()

    pub = Publishing()
    pub.title='test-Title'
    pub.date_from='16.11.18'
    pub.date_until = '16.11.18'
    pub.link_url = 'anything'
    pub.description = 'This is a test for the stats plugins'
    pub.image_url = 'image url'
    pub.state = 1
    pub.channel_id='Gcal'

    c = db.session.query(Channel).first()
    c_conf = c.config
    gcal_plugin.run(pub, c_conf)

    k2 = stats.number_of_posts() -1

    assert k==k2

#We look first the number of post and then we publish a post and then we relook if the number of post is +1
def test_FB_post():

    k = stats.number_of_posts()

    msg = "This is a publication test"
    api = get_api(CFG)
    publication_id = publish(msg)

    k2 = stats.number_of_posts() -1

    assert k==k2
