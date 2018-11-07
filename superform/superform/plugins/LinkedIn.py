import json
import traceback

from flask import request, render_template
from linkedin import linkedin  # from python3-linkedin library

FIELDS_UNAVAILABLE = ['Title', 'Description']

CONFIG_FIELDS = []  # Unused for now. But could be used to refresh dynamically the access token


def linkedin_plugin(id, c, m, clas, config_fields):
    """
    Launched by channels.configure_channel(id) when the configure page
    is reached and the channel is from the LinkedIn module. It creates
    the REDIRECT_LINK which is used in the linkedin_configuration.html
    and calls the render_template() function.
    """
    state = "id_" + str(id) + "rest_12345"
    RETURN_URL = 'http://localhost:5000/configure/linkedin'
    CLIENT_ID = '77p0caweo4t3t9'
    CLIENT_SECRET = 'uQVYTN3pDewuOb7d'
    REDIRECT_LINK = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=" \
                    + CLIENT_ID + "&redirect_uri=" + RETURN_URL + "&state=" + state
    RETURN_URL += str(id)
    return render_template("linkedin_configuration.html",
                           channel = c,
                           config_fields = config_fields,
                           redirect = REDIRECT_LINK)


def get_basic_authentication():
    """ Get the access to the LinkedIn account and links to the
     python3-linkedin library """
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

    authentication = get_basic_authentication()
    print("code I put in authentification", code)
    authentication.authorization_code = code
    access_token = get_access_token(authentication)
    if access_token is not None:
        print("Access Token:", access_token.access_token)
        print("Expires in (seconds):", access_token.expires_in)
        return access_token
    return None


def get_access_token(authentication):
    try:
        access_token = authentication.get_access_token()
        return access_token
    except linkedin.LinkedInError as err:
        print("A fault occurred while getting the access token")
        traceback.print_exc()
        return None


def run(publishing, channel_config):
    """ Gathers the informations in the config column and launches the
    posting process """
    json_data = json.loads(channel_config)
    token = json_data['token']
    title = publishing.title
    body = publishing.description  # a quoi tu sers?
    link = publishing.link_url

    comment = title + "\n" + body + "\n" + link
    print("Body: ", body)
    print("Title: ", title)
    print("Link: ", link)

    posted = post(token, comment = comment, title = None, description = None,
                  submitted_url = None, submitted_image_url = None)
    if posted is not None:
        print("Post successful")
    else:
        print("The post failed")


def post(access_token, comment = None, title = None, description = None,
         submitted_url = None, submitted_image_url = None,
         visibility_code = 'anyone'):
    """
    Publishes the post using the python3-linkedin API
    :param access_token: the access token which allows publishing
    :param comment: the body of the article
    :param title: the title of the related image or link
    :param description:
    :param submitted_url: the link
    :param submitted_image_url: the image
    :param visibility_code: visibility of the post on LinkedIn (on
    'anyone' by default
    :return: returns the link to the post just created or an exception
    """
    import collections
    AccessToken = collections.namedtuple('AccessToken',
                                         ['access_token', 'expires_in'])
    authentication = get_basic_authentication()
    authentication.token = AccessToken(access_token, "99999999")
    application = linkedin.LinkedInApplication(authentication)
    profile = application.get_profile()
    print("User Profile", profile)
    try:
        resp = application.submit_share(comment, title, description,
                                        submitted_url, submitted_image_url,
                                        visibility_code)
        return resp
    except Exception as e:
        print(e)
        return False
