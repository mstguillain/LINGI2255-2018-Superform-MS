import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from flask import current_app
import json
import traceback
from linkedin import linkedin

from flask import Blueprint, current_app, url_for, request, make_response, \
    redirect, session, render_template

from superform.utils import login_required, get_instance_from_module_path, \
    get_modules_names, get_module_full_name
from superform.models import db, Channel
import ast

# channels_page = Blueprint('channels', __name__)

# from flask_oauthlib.client import OAuth

# THIS IT THE GOOD ONE

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
                           channel=c,
                           config_fields=config_fields,
                           redirect=REDIRECT_LINK)


def get_basic_autantication():
    """

    :return:
    """
    CLIENT_ID = '77p0caweo4t3t9'
    CLIENT_SECRET = 'uQVYTN3pDewuOb7d'
    RETURN_URL = 'http://localhost:5000/configure/linkedin'

    authentication = linkedin.LinkedInAuthentication(
        CLIENT_ID,
        CLIENT_SECRET,
        RETURN_URL,
        linkedin.PERMISSIONS.enums.values()
    )
    return authentication


def linkedin_use(code):
    """
    Use the authorization token to generate the
    :param code: the authorization_code gotten from the api
    :return: the gotten access token
    """
    print("From linkedin.py: " + code)

    authentication = get_basic_autantication()
    print("code I put in authentification", code)
    authentication.authorization_code = code
    acces_token = get_access_token(authentication)
    if acces_token is not None:
        print("Access Token:", acces_token.access_token)
        print("Expires in (seconds):", acces_token.expires_in)
        return acces_token
    return None


def get_access_token(authentication):
    try:
        access_token = authentication.get_access_token()
        return access_token
    except linkedin.LinkedInError as err:
        print("A fault occurred while getting the acess token")
        traceback.print_exc()
        return None


# TODO to change according to the api
def run(publishing, channel_config):
    json_data = json.loads(channel_config)
    # login = json_data['login']
    # password = json_data['password']
    token = json_data['token']
    title = publishing.title
    body = publishing.description  # a quoi tu sers?
    link = publishing.link_url

    comment = title + "\n" + body + "\n" + link
    print("Body: ", body)
    print("Title: ", title)
    print("Link: ", link)
    # msg.attach(MIMEText(body, 'plain'))

    posted = post(token, comment=comment, title=None, description=None, submitted_url=None, submitted_image_url=None)
    if posted is not None:
        print("Post sucessfull")
    else:
        print("The post failed")


def post(access_token, comment=None, title=None, description=None,
         submitted_url=None, submitted_image_url=None,
         visibility_code='anyone'):
    """

    :param access_token: the access token which allows publishing
    :param comment: the body of the article
    :param title: the title of the related image or link
    :param description: the over
    :param submitted_url: the link
    :param submitted_image_url: the
    :param visibility_code:
    :return:
    """
    import collections
    AccessToken = collections.namedtuple('AccessToken', ['access_token', 'expires_in'])
    authentication = get_basic_autantication()
    authentication.token = AccessToken(access_token, "99999999")
    application = linkedin.LinkedInApplication(authentication)
    profile = application.get_profile()
    print("User Profile", profile)
    try:
        resp = application.submit_share(comment, title, description, submitted_url, submitted_image_url,
                                        visibility_code)
        return resp
    except Exception as e:
        print(e)
        return False

##########################
# keep this just in case #
##########################
# redirect1 = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77p0caweo4t3t9&redirect_uri=http://localhost:5000/%2Fauth%2Flinkedin&state=987654321&'
# redirect1bis = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=", CLIENT_ID, "&redirect_uri=", RETURN_URL, "%2Fauth%2Flinkedin&state=", state, "&"
# redirect2 = "https://www.linkedin.com/oauth/v2/accessToken?grant_type=client_credentials&client_id=77p0caweo4t3t9&client_secret=uQVYTN3pDewuOb7d"
# not allowed to create application tokens
