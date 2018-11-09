from __future__ import print_function
from flask import current_app, session, flash
from superform.models import db, User
import json
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


FIELDS_UNAVAILABLE = ['Image']

def get_user_credentials():
    user = User.query.get(session["user_id"])
    return client.OAuth2Credentials.from_json(json.loads(user.gcal_cred)) if user.gcal_cred else None

def set_user_credentials(creds):
   user = User.query.get(session["user_id"])
   user.gcal_cred = creds.to_json().stringify()

def run(publishing, channel_config):
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    creds = get_user_credentials()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, file.Storage('token.json'))
        set_user_credentials(creds)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    event = {
        'summary': publishing.title,
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': publishing.description,
        'start': {
            'dateTime': '2018-11-15T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2018-12-15T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    id = publish(event,service)

def publish(event,service):
    """
    Publie sur le compte et renvoie l'id de la publication
    """

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink'))) #TODO Delete when finished debugging
    return event.get('htmlLink')

def delete(id):
    """
    Supprime la publication
    """
