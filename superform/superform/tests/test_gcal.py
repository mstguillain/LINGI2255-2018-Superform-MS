from datetime import datetime, timedelta
from superform.plugins import gcal_plugin
from superform import app, db, User, Publishing, channels, Post
from superform.models import Channel, db
from googleapiclient.discovery import build
from superform.tests.test_basic import client, login, write_to_db, create_user, create_channel, create_auth
from superform.utils import get_module_full_name
import pytest, random, string, json


def setup_db(channel_name, channel_module):
    gcal_config = {'project_id':'superform-1541421444976',
              'client_id':'886003916698-2pig0lv6eslba41vrfrefnovmlqpsk3i.apps.googleusercontent.com',
              'client_secret':'Txqi7eqzfGflL3U5PntpGBqV'}

    user = create_user(id=10, name="test10", first_name="utilisateur10", email="utilisateur10.test@uclouvain.be")
    gcal_plugin.generate_user_credentials(json.dumps(gcal_config), user.id)
    channel = create_channel(channel_name, channel_module, gcal_config)
    
    post = basic_post(user.id)
    write_to_db(post)
    pub = publish_from_post(post)
    write_to_db(pub)
    return user, channel, post, pub

def basic_post(user_id, title=None, delta=timedelta(hours=1)):
    post = Post()
    post.user_id = user_id
    post.title = title if title else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    post.description = 'This is a test !'
    post.date_from = datetime.now() + timedelta(days=1)
    post.date_until = post.date_from + delta
    return post
  
def publish_from_post(post):
    pub = Publishing()
    pub.post_id = post.id
    pub.title = post.title
    pub.description = post.description
    pub.date_from = post.date_from
    pub.date_until = post.date_until
    pub.state = 0
    pub.channel_id = 'gcal_plugin'
    return pub

def basic_publish(title=None, delta=timedelta(hours=1)):
    pub = Publishing()
    pub.title = title if title else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    pub.description = 'This is a test !'
    pub.date_from = datetime.now() + timedelta(days=1)
    pub.date_until = pub.date_from + delta
    pub.state = 0
    pub.channel_id = 'gcal_plugin'
    return pub



#tries to publish an event by using the run function of the gcal_plugin and
# then will check if it was actually published by getting the list of all published events.
def test_run_gcal(client):
    user, channel, post, pub = setup_db(channel_name='test_gcal', channel_module='gcal_plugin')
    login(client, user.id)
    rv = client.post('/moderate/' + str(post.id) + '/' + str(channel.name))

    creds = gcal_plugin.get_user_credentials(user.id)
    service = build('calendar', 'v3', credentials=creds)
    events = service.events().list(calendarId='primary',pageToken=None, timeMin=pub.date_from, timeMax=pub.date_until).execute()
    found = False
    for event in events['items']:
        if(event['summary'] == pub.title):
            found=True
    assert found

def test_validity_title_gcal():
    pub = basic_publish(title='    ')
    assert gcal_plugin.is_valid(pub) == False

def test_validity_datetime_gcal():
    pub = basic_publish(delta=timedelta(days=-1))
    assert gcal_plugin.is_valid(pub) == False

def test_validity_gcal():
    pub = basic_publish() 
    assert gcal_plugin.is_valid(pub) == True


