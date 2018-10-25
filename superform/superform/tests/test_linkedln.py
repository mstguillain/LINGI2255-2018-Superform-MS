import datetime
import os
import tempfile
import traceback
import pytest
from linkedin import linkedin

from superform import app, db
from superform.plugins import mail


## pip install python-linkedin
## log in : tip.hon2014@gmail.com
## pwd : PwdForTeam06

@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


authorization_code = "AQTPNbuFxfPw7REPJppr-1m3erCFDDJek21lsLWoLX1cDKdCB7fdjYyfGlBfGxippwiL2blrubQZyxo17HISoOayzHQ2fMlkPLlUxFMRoAntFbEJxMkbZMJyHsVe2uJx8eK1HjbpXTFhcsik8Pa_9Jneb1DqBWYgP9YZbZpVRgNs2yFT7O1LftZ6PbK5yQ"
acces_token = "AQXDaUq7kmBz1CvrShflgk_mFRlXYq9tHHVgUzgGnGcvQEt7Pag2XtGgZiEnenjlZk1zrQXiEAB-U92SBoQVdNWKfx6LDcPVCJX4yRNyM7c0icEGexYqAQcFKRTnyflTgBuFo2ozTeuTwOY4xFe1iW51-Ph9cD25GVEHFapMVRj2oz-o2dkxanAW-cnzrQSkccOiW_aIrJqH-WsS37viS91mTRK9syXJbvCMHu4GwI4BwUsUJ9pfaal3X1U0Dmy-LmgnvHNW7utMZQdhUa2v7mTaIebdkXYJ__39p-OzIUXnDA_KtFHMsCj14PZ1lQTkGSO4dnkP7kx2VP8pLJRoyKuQWoUONA"


def is_connected():
    """Return true if acess_token is present and not expired"""
    return len(get_access_token()) > 1


def has_authorization_code():
    """ Return true if there is an authorizaton code, allowing us to direclty get the acess_token if not expired"""
    return len(authorization_code) > 1


def get_authorization_code():
    return authorization_code


def get_authentication_url(redirect_url="http://localhost:5000"):
    """The url the user should be redirected to for login in"""
    redirection = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77p0caweo4t3t9&redirect_uri=" + redirect_url + "/&state=12345"
    return redirection


def redirect_to(url):
    """Redirect the user to the given url"""
    ## TODO : use something like window.redirect or window.pop_up
    pass


def set_acess_token(authentication):
    try:
        acces_token = authentication.get_access_token()
        return True
    except linkedin.exceptions.LinkedInError as err:
        print("A fault occurred while getting the acess token")
        traceback.print_exc()
        return False


def get_access_token():
    return acces_token


def get_basic_authentication(RETURN_URL='http://localhost:5000/'):
    CLIENT_ID = '77p0caweo4t3t9'
    CLIENT_SECRET = 'uQVYTN3pDewuOb7d'
    # TODO the configure url, to be changed on the LinkeIn Application service
    state = '12345'
    authentication = linkedin.LinkedInAuthentication(
        CLIENT_ID,
        CLIENT_SECRET,
        RETURN_URL,
        linkedin.PERMISSIONS.enums.values()
    )
    authentication.authorization_code = "AQQAT26rbiHMp77ucRO-C3ofII05htPBBKXy47fvHz8SjNizA_2dxCKSzij3pzmjsgVsVvNZ0l4Elmo9yb6tqcN-3NImm9JzJABmPWONpcHurCR-K9JSvvX4bjTkmeK3es57rHXNNLFnmpBYkjyVxIcFMWhuvV5klfZb0Vh9NbYHdfMxCtcVXWmJktKcCg"

    return authentication


def has_been_redirected(uri):
    ## TODO : find a way to get the current URI after the redirection and use it to get the autorization code
    pass


def post(authentication, message='Testing the api'):
    import collections
    AccessToken = collections.namedtuple('AccessToken', ['access_token', 'expires_in'])
    authentication.token = AccessToken(get_access_token(), "99999999")
    application = linkedin.LinkedInApplication(authentication)
    profile = application.get_profile()
    print("Profile", profile)
    resp = application.submit_share("comment", "title", "description", None,
                                    None)
    print("Resp", resp)
    return True


def login():
    ## application = linkedin.LinkedInApplication(authentication)
    ## Check if connected
    if is_connected():
        authentication = get_basic_authentication()
        authentication.authorization_code = get_authorization_code()
        post(authentication)
        return True
    print("Not connected")
    ## Check if can be connected rapidly

    if has_authorization_code():
        authentication = get_basic_authentication()
        authentication.authorization_code = get_authorization_code()
        if set_acess_token(authentication):
            return True

    ## Do the full login operation
    authentication = get_basic_authentication()
    auth_url = get_authentication_url(authentication.redirect_uri)
    ## Redirect the user to that URL so we can get the authorization token
    redirect_to(auth_url)

    ## The code follows in has_been_redirected


def test_run_linkedinl(client):
    # Is there a way to test a send mail function?
    login()

    print("======================")
    # print(str(application.get_statistics_company_page(674969)))
    print("token :", get_access_token())
    print("======================")
    assert True == True
