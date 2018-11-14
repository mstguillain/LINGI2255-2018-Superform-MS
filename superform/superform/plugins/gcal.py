from flask import session
from superform.models import db, User
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json


FIELDS_UNAVAILABLE = ['Image']
PROJECT_ID = 'project_id'
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
CONFIG_FIELDS = [PROJECT_ID, CLIENT_ID, CLIENT_SECRET]


def creds_to_string(creds):
   return json.dumps({'token': creds.token,
            'refresh_token': creds._refresh_token,
            'token_uri': creds._token_uri,
            'client_id': creds._client_id,
            'client_secret': creds._client_secret,
            'scopes': creds._scopes})

def get_user_credentials():
   user = User.query.get(session["user_id"])
   return Credentials.from_authorized_user_info(json.loads(user.gcal_cred)) if user.gcal_cred else None

def set_user_credentials(creds):
   user = User.query.get(session["user_id"])
   user.gcal_cred = creds_to_string(creds)
   db.session.commit()

def get_full_config(channel_config):
   return {"installed":{"client_id":channel_config[CLIENT_ID],
                "project_id":channel_config[PROJECT_ID],
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://www.googleapis.com/oauth2/v3/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":channel_config[CLIENT_SECRET],
                "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}

def generate_event(publishing):
   return {
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

def run(publishing, channel_config):
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    creds = get_user_credentials()
    if not creds:
       channel_config = get_full_config(json.loads(channel_config))
       flow = InstalledAppFlow.from_client_config(channel_config, scopes=[SCOPES])
       creds = flow.run_local_server(host='localhost', port=8080,
                   authorization_prompt_message='Please visit this URL: {url}',
                   success_message='The auth flow is complete, you may close this window.',
                   open_browser=True)
       set_user_credentials(creds)

    service = build('calendar', 'v3', credentials=creds)
    event = generate_event(publishing)
    id = publish(event, service)

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
