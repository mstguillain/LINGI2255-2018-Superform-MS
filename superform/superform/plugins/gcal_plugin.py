from __future__ import print_function
from flask import current_app, session, flash
from superform.models import db, User
import json
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["page_id"]

CFG = {
    "page_id": "UNDEFINED",  # Step 1
    "access_token": "UNDEFINED"
}


def run(publishing, channel_config):
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=20, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


    # On chope le message dans le champ description du post.
    title = publishing.title
    body = publishing.description
    link = publishing.link_url
    image = publishing.image_url
    date_begin = publishing.date_from
    date_end = publishing.date_until

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


def setToken(goal_page_id):
    user = User.query.get(session["user_id"])
    credentials = user.fb_cred
    print(credentials)
    if credentials != None:
        splitted = credentials.split(",")  # Split fb_cred to give us tuple page_id|access_token
        for elem in splitted:
            page_and_token = elem.split("|")  # Split page_id|access_token
            if (page_and_token[0] == goal_page_id):  # If page id from credentials is the one we're looking for
                return page_and_token[1]
    else:
        flash('please log out and login, no facebook token found on the database')
    return "ACCESS_TOKEN_NOT_FOUND"
