import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from flask import current_app
import json


# from linkedin import linkedin

#######################
# Copied from mail.py #
#######################

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = ["account", "login"]


# TODO to change according to the api
def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    account = json_data['account']
    login = json_data['login']
    msg = MIMEMultipart()
    msg['From'] = account
    msg['To'] = login
    msg['Subject'] = publishing.title

    body = publishing.description
    msg.attach(MIMEText(body, 'plain'))

    try:
        smtpObj = smtplib.SMTP(current_app.config["SMTP_HOST"],
                               current_app.config["SMTP_PORT"])
        if current_app.config["SMTP_STARTTLS"]:
            smtpObj.starttls()
        text = msg.as_string()
        smtpObj.sendmail(account, login, text)
        smtpObj.quit()
    except SMTPException as e:
        # TODO should add log here
        print(e)


########################################################
# Taken from https://pypi.org/project/python-linkedin/ #
########################################################

#def login():
#    CONSUMER_KEY = "77p0caweo4t3t9"
#    CONSUMER_SECRET = "uQVYTN3pDewuOb7d"
#    USER_SECRET="" ?
#    USER_TOKEN="" ?
#    RETURN_URL = 'http://localhost:5000'
#
#
# Define CONSUMER_KEY, CONSUMER_SECRET,
# USER_TOKEN, and USER_SECRET from the credentials
# provided in your LinkedIn application

# Instantiate the developer authentication class

#authentication = linkedin.LinkedInDeveloperAuthentication(
#                    CONSUMER_KEY,
#                    CONSUMER_SECRET,
#                    USER_TOKEN,
#                    USER_SECRET,
#                    RETURN_URL,
#                    linkedin.PERMISSIONS.enums.values()
#                )

# Optionally one can send custom "state" value that will be returned from OAuth server
# It can be used to track your user state or something else (it's up to you)
# Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it

# authorization.state = 'your_encoded_message'

# Pass it in to the app...

# application = linkedin.LinkedInApplication(authentication)

# Use the app....

# application.get_profile()