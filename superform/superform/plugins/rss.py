import feedparser
from flask import current_app
import json

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = ["sender", "receiver"]


def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    sender = json_data['sender']
    receivers = json_data['receiver']
    title = publishing.title
    body = publishing.description
