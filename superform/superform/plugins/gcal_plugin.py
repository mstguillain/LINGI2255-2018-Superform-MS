from flask import session
from superform.models import db, User
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import inspect


FIELDS_UNAVAILABLE = ['Image']
CREDENTIALS = '/Users/laurent/Documents/LINGI2255/LINGI2255-2018-Superform-MS-02/superform/superform/credentials.json'


def creds_to_string(creds):
   return json.dumps({'token': creds.token,
            'refresh_token': creds._refresh_token,
            'token_uri': creds._token_uri,
            'client_id': creds._client_id,
            'client_secret': creds._client_secret,
            'scopes': creds._scopes})

def get_user_credentials():
   user = User.query.get(session["user_id"])
   dict = json.loads(user.gcal_cred)
   return Credentials.from_authorized_user_info(dict) if user.gcal_cred else None

def set_user_credentials(creds):
   user = User.query.get(session["user_id"])
   user.gcal_cred = creds_to_string(creds)
   db.session.commit()

def run(publishing, channel_config):
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    creds = get_user_credentials()
    if not creds or not creds.valid:
       flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, scopes=[SCOPES])
       creds = flow.run_local_server(host='localhost', port=8080,
                   authorization_prompt_message='Please visit this URL: {url}',
                   success_message='The auth flow is complete, you may close this window.',
                   open_browser=True)
       set_user_credentials(creds)

    service = build('calendar', 'v3', credentials=creds)
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

def publish(event, service):
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
