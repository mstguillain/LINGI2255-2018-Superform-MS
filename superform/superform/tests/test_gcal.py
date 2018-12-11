from datetime import datetime
from superform.plugins import gcal_plugin
from superform import app, db, Publishing, channels
from superform.models import Channel, db
from googleapiclient.discovery import build

#tries to publish an event by using the run function of the gcal_plugin and
# then will check if it was actually published by getting the list of all published events.
def test_run():
    pub = Publishing()
    pub.title='test-Title'
    pub.date_from='16.11.18'
    pub.date_until = '16.11.18'
    pub.link_url = 'anything'
    pub.description = 'description'
    pub.image_url = 'image url'
    pub.state = 1
    pub.channel_id='Gcal'

    c = db.session.query(Channel).first()
    c_conf = c.config
    gcal_plugin.run(pub, c_conf)

    new_date = datetime.datetime(2018, 11, 16)
    creds = gcal_plugin.get_user_credentials()
    service = build('calendar', 'v3', credentials=creds)
    events = service.events().list(calendarId='primary',pageToken=None, timeMin=new_date,timeMax=new_date).execute()
    found = False
    for event in events['items']:
        if(event['summary']=='test-Title'):
            found=True
    print(found)
    assert found

def test_validity_title():
    pub = Publishing()
    pub.title = ' '
    pub.date_from = '16.11.18'
    pub.date_until = '16.11.18'
    pub.link_url = 'anything'
    pub.description = 'description'
    pub.image_url = 'image url'
    pub.state = 1
    pub.channel_id = 'Gcal'

    result = gcal_plugin.is_valid(pub)
    assert result==False

def test_validity_date():
    pub = Publishing()
    pub.title = 'test'
    pub.date_from = '16.11.1995'
    pub.date_until = '16.11.1995'
    pub.link_url = 'anything'
    pub.description = 'description'
    pub.image_url = 'image url'
    pub.state = 1
    pub.channel_id = 'Gcal'

    result = gcal_plugin.is_valid(pub)
    assert result==False

def test_validity():
    pub = Publishing()
    pub.title = 'test'
    pub.date_from = '16.11.18'
    pub.date_until = '16.11.18'
    pub.link_url = 'anything'
    pub.description = 'description'
    pub.image_url = 'image url'
    pub.state = 1
    pub.channel_id = 'Gcal'

    result = gcal_plugin.is_valid(pub)
    assert result==True


