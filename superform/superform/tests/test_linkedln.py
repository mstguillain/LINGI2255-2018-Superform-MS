import datetime
import os
import tempfile
import traceback
import pytest
from linkedin import linkedin
import json
import random

from superform import app, Publishing
from superform.plugins import LinkedIn
from superform.models import Channel, db

#########################
## test on credentials ##
#########################
import configparser
from pathlib import Path

## pip install python-linkedin
## log in : tip.hon2014@gmail.com
## pwd : PwdForTeam06


"""
    Global variables witch should be able to be accessed from everywhere 
"""
plugin_path_name = "superform/plugins"
ini_file_name = "linkedin.ini"
url_root = "localhost:5000/" #hardcoded for local tests but should be changed for test in a deployed version


def test_run_linkedin():
    """
    Checks if a simple linkedin post can be created (require a testchannel in the DB)
    Since it was not possible to directly call the LinkedIn.run methode from here (using requests and dynamic url).
    We basically code again the LinkedIn.run methode in a more "harcoded" way but it's
    exactly the same as the LinkedIn.run method
    """
    pub = Publishing()
    pub.date_from = '13.02.02'
    pub.title = 'test-Title'
    pub.link_url = 'a link'
    determinants = ["une", "un", "le", "la", "les", "vos", "nos", "mes", "tes"]
    nomCommuns = ["chien", "chat", "vache", "cheval", "poney", "cochon", "poule", "coq"]
    verbes = ["aller", "venir", "courir", "voler", "manger", "mourir", "partir", "skier"]
    lieux = ["campagne", "montagne", "aeroport", "ecole", "mer", "jardin", "toilette"]
    testDeterminant = determinants[random.randint(0,8)]
    testNomCmmun = nomCommuns[random.randint(0,7)]
    testVerbe = verbes[random.randint(0,7)]
    testLieu = lieux[random.randint(0,6)]
    pub.description = " " + testDeterminant + " " + testNomCmmun +" "+ testVerbe + " "+ testLieu + " " + str(random.randint(0,10000))
    pub.image_url = 'image url'
    pub.date_until = '14.02.19'
    pub.state = 1
    print("The  LinkedIn posting test has started...")
    linkedIn_Channel = db.session.query(Channel).filter(
        Channel.name=="TestLinkedInDoNotDelete").first()
    if (linkedIn_Channel is None):
           assert(False), "LinkedIn test_run requires the DB to have a testChannel named TestLinkedInDoNotDelete"
    else:
        channel_config = linkedIn_Channel.config
        pub.channel_id = linkedIn_Channel.id
        json_data = json.loads(channel_config)
        access_token = json_data['token']
        title = pub.title
        body = pub.description
        link = pub.link_url

        comment = title + "\n" + body + "\n" + link
        import collections
        AccessToken = collections.namedtuple('AccessToken',
                                             ['access_token', 'expires_in'])

        try:
            client_id = LinkedIn.get_client_id()
        except FileNotFoundError:
            client_id = None
            assert (False), "bad configuration, requires a linkedin.ini file "
        try:
            client_secret = LinkedIn.get_client_secret()
        except FileNotFoundError:
            client_secret = None
            assert (False), "bad configuration, requires a linkedin.ini file "

        return_url = url_root+"/channels"
        authentication = linkedin.LinkedInAuthentication(
            client_id,
            client_secret,
            return_url,
            linkedin.PERMISSIONS.enums.values()
        )

        assert(authentication is not None), "LinkedIn.LinkedInAuthentification failed"
        authentication.token = AccessToken(access_token, "99999999")
        application = linkedin.LinkedInApplication(authentication)
        status=""
        try:
            resp = application.submit_share(comment, title, description=None,
                                            submitted_url=None, submitted_image_url=None,
                                            visibility_code='anyone')
            status = "Success publishing"
        except Exception as e:
            print(e)
            status = "Error publishing. The testChannel (named TestLinkedInDoNotDelete) may be banned for spamming)" \
                     + "\n" +"if so, go to the channel config and relink it to a non-valuable linkedIn account"




        assert status == "Success publishing", "Couldn't post on LinkedIn"


def test_config_sections():
    """
    Test whether the config_parser works
    """
    config= configparser.ConfigParser()
    config.read('test.ini')
    str = config.get('Credentials', 'CLIENT_ID')
    assert str=="myclientID"


def test_get_linkedin_ini_exception():
    """
    Tests whether the exception is well raised
    TODO: since the get_linkedin_ini method only check one place (plugins) the
    only way to test it is by removing the .ini file in plugins. For now, the
    test makes no sense.
    TODO: to test (jean : can't we just rename the file before the test and then rename it again after the test ? ,
    we could also test if the file is there ourself, then wait for an expection or not according to the answer
    """
    print("The initialization exceptions tests have started...")
    file_not_found = False
    try:
        test_get_linkedin_ini()
    except AssertionError:
        print("The ini file or directory was not found, testing the that an exception is raised accordingly...")
        file_not_found = True

    if file_not_found:
        with pytest.raises(FileNotFoundError, message="A file not found exception was not thrown"):
            LinkedIn.get_linkedin_ini()
            # TODO: Print that everything went well if the exception was well caught

    else:
        print("No init error occurred")
        # TODO: test that the initialization doesn't throw an erro


def test_get_linkedin_ini():
    """
    Tests whether the linkedin.ini file is present in the plugins folder
    TODO: to test (yash: i was unable to run the tests)
    """
    data_folder = Path(plugin_path_name)
    assert data_folder.is_dir(), "Couldn't find the directory folder for plugins at the path " + plugin_path_name + "\n"
    final_path = plugin_path_name + "/" +ini_file_name
    file_to_open = Path(final_path)
    assert file_to_open.is_file(), "Couldn't find the file " + ini_file_name + " the module won't be initialised properly" + "\n"


def test_get_client_id_and_secret():
    """
    Tests whether we find the right values in the test.ini file
    TODO: to test (yash: i was unable to run the tests)
    """
    print("Testing the client id and the secret...")
    config = configparser.ConfigParser()
    config.read('test.ini')
    c_id = config.get('Credentials', 'CLIENT_ID')
    c_secret = config.get('Credentials', 'CLIENT_SECRET')
    myhobby = config.get('Profile_1', 'hobby')
    assert c_id == "myclientID", "the client id is wrong"
    assert c_secret == "myclientsecret", "the secret is wrong"
    assert myhobby == 'bass', "the profile is wrong "
