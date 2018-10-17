import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from flask import current_app
from linkedin import linkedin
import json

#######################
# Copied from mail.py #
#######################

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = ["sender", "receiver"]


def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    sender = json_data['sender']
    receivers = json_data['receiver']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = publishing.title

    body = publishing.description
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtpObj = smtplib.SMTP(current_app.config["SMTP_HOST"],
                               current_app.config["SMTP_PORT"])
        if current_app.config["SMTP_STARTTLS"]:
            smtpObj.starttls()
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        smtpObj.quit()
    except SMTPException as e:
        # TODO should add log here
        print(e)


########################################################
# Taken from https://pypi.org/project/python-linkedin/ #
########################################################

API_KEY = "77p0caweo4t3t9"
API_SECRET = "uQVYTN3pDewuOb7d"
RETURN_URL = "http://localhost:8000"
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET,
                                                 RETURN_URL,
                                                 linkedin.PERMISSIONS.enums.values())
print(authentication.authorization_url)
application = linkedin.LinkedInApplication(authentication)
