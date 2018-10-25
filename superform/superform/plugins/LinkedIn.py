import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from flask import current_app
import json
import  traceback
from linkedin import linkedin

from flask import Blueprint, current_app, url_for, request, make_response, \
    redirect, session, render_template

from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name
from superform.models import db, Channel
import ast

# channels_page = Blueprint('channels', __name__)

# from flask_oauthlib.client import OAuth

#######################
# Copied from mail.py #
#######################

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = ["Login", "Password"]  # TODO do we keep it?


# The return_url must be changed on the LinkedIn Application service
# Is it possible to return to the /configure/<id> webpage? Where to analyse the GET request (request.get() ?)


def linkedin_plugin(id, c, m, clas, config_fields):
    """Launched by channels.configure_channel(id)"""
    state = "id_" + str(id) + "rest_12345"
    RETURN_URL = 'http://localhost:5000/configure/linkedin'
    CLIENT_ID = '77p0caweo4t3t9'
    CLIENT_SECRET = 'uQVYTN3pDewuOb7d'
    REDIRECT_LINK = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=" + CLIENT_ID + "&redirect_uri=" + RETURN_URL + "&state=" + state
    if request.url.startswith("yolo"):
        pass  # TODO take what's after the code
    RETURN_URL += str(id)
    return render_template("linkedin_configuration.html",
                           channel = c,
                           config_fields = config_fields,
                           redirect = REDIRECT_LINK)
    # TODO find a way to read the url and store the code
    # request.get() ?

    # redirection = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=" + CLIENT_ID + "&redirect_uri=" + RETURN_URL + "&state=" + state

    # TODO user redirected to redirection
    # TODO testing the returned state value




def linkedin_use(code):
    print("From linkedin.py: "+code)
    CLIENT_ID = '77p0caweo4t3t9'
    CLIENT_SECRET = 'uQVYTN3pDewuOb7d'
    RETURN_URL = 'http://localhost:5000/configure/linkedin'

    authentication = linkedin.LinkedInAuthentication(
        CLIENT_ID,
        CLIENT_SECRET,
        RETURN_URL,
        linkedin.PERMISSIONS.enums.values()
    )
    print("code I put in authentification", code)
    authentication.authorization_code = code
    acces_token = get_access_token(authentication)
    if acces_token is not None:
        print("Access Token:", acces_token.access_token)
        print("Expires in (seconds):", acces_token.expires_in)




def get_access_token(authentication):
    try:
        access_token = authentication.get_access_token()
        return access_token
    except linkedin.LinkedInError as err:
        print("A fault occurred while getting the acess token")
        traceback.print_exc()
        return None

# TODO to change according to the api
# def run(publishing, channel_config):
#    json_data = json.loads(channel_config)
#    account = json_data['account']
#    login = json_data['login']
#    msg = MIMEMultipart()
#    msg['From'] = account
#    msg['To'] = login
#    msg['Subject'] = publishing.title
#
#    body = publishing.description
#    msg.attach(MIMEText(body, 'plain'))
#
#    try:
#        smtpObj = smtplib.SMTP(current_app.config["SMTP_HOST"],
#                               current_app.config["SMTP_PORT"])
#        if current_app.config["SMTP_STARTTLS"]:
#            smtpObj.starttls()
#        text = msg.as_string()
#        smtpObj.sendmail(account, login, text)
#        smtpObj.quit()
#    except SMTPException as e:
#        # TODO should add log here
#        print(e)

##########################
# keep this just in case #
##########################
# redirect1 = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77p0caweo4t3t9&redirect_uri=http://localhost:5000/%2Fauth%2Flinkedin&state=987654321&'
# redirect1bis = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=", CLIENT_ID, "&redirect_uri=", RETURN_URL, "%2Fauth%2Flinkedin&state=", state, "&"
# redirect2 = "https://www.linkedin.com/oauth/v2/accessToken?grant_type=client_credentials&client_id=77p0caweo4t3t9&client_secret=uQVYTN3pDewuOb7d"
# not allowed to create application tokens

#########################################################
# Taken from https://pypi.org/project/python3-linkedin/ #
#########################################################
#
# from linkedin import linkedin
#
# authentication = linkedin.LinkedInAuthentication(CLIENT_ID, CLIENT_SECRET,
#                                                 RETURN_URL,
#                                                 linkedin.PERMISSIONS.enums.values())
# print(authentication.authorization_url)
# application = linkedin.LinkedInApplication(authentication)
#
# Define CONSUMER_KEY, CONSUMER_SECRET,
# USER_TOKEN, and USER_SECRET from the credentials
# provided in your LinkedIn application
#
# Instantiate the developer authentication class
#
#   authentication = linkedin.LinkedInDeveloperAuthentication(
#      CONSUMER_KEY,
#      CONSUMER_SECRET,
#      USER_SECRET,
#   RETURN_URL,
# linkedin.PERMISSIONS.enums.values()
# )
#
# Optionally one can send custom "state" value that will be returned from OAuth server
# It can be used to track your user state or something else (it's up to you)
# Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
#
# authorization.state = 'your_encoded_message'
#
# Pass it in to the app...
#
#   application = linkedin.LinkedInApplication(authentication)

# Use the app....

#  application.get_profile()
