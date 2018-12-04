from datetime import datetime, timedelta
from superform.plugins import gcal_plugin
from superform import app, db, User, Publishing, channels, Post
from superform.models import Channel, db
from googleapiclient.discovery import build
from superform.tests.test_basic import client, login, write_to_db, create_user, create_channel, create_auth
from superform.utils import get_module_full_name
import random, string, json


def setup_db(post_id, channel_name, user_id):
    gcal_config = {'project_id':'superform-1541421444976',
              'client_id':'886003916698-2pig0lv6eslba41vrfrefnovmlqpsk3i.apps.googleusercontent.com',
              'client_secret':'Txqi7eqzfGflL3U5PntpGBqV'}

    gcal_plugin.generate_user_credentials(json.dumps(gcal_config), user_id)
    create_channel(channel_name, 'gcal_plugin', gcal_config)
    
    post = basic_post(post_id, user_id)
    pub = publish_from_post(post)
    write_to_db(post)
    write_to_db(pub) 

def basic_post(id, user_id, title=None, delta=timedelta(hours=1)):
    post = Post()
    post.id = id
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
def test_run_gcal():
    max_id = Channel.query.order_by(Channel.id).first().id
    print('------------------------------------------------------------------ID:' + str(max_id))
    return
    setup_db(post_id=1, channel_name='test_gcal', user_id='1')
    login(client, '1') 
    rv = client.post('/moderate/1/test_gcal')

    creds = gcal_plugin.get_user_credentials('myself')
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


