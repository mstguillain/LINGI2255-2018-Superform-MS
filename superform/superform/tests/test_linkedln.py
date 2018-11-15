import datetime
import os
import tempfile
import traceback
import pytest
from linkedin import linkedin
import json

from superform import app, db, Publishing, channels
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
ini_file_name = "lindekin.ini"


def test_run_linkedin():
    """
    Checks if a simple linkedin post can be created (require a session being present in the db)
    :return:
    """
    pub = Publishing()
    pub.date_from = '13.02.02'
    pub.title = 'test-Title'
    pub.link_url = 'a link'
    pub.description = 'descr'
    pub.image_url = 'image url'
    pub.date_until = '14.02.19'
    pub.state = 1
    print("The  LinkedIn posting test has started...")
    linkedIn_Channel = db.session.query(Channel).filter(
        Channel.module == "superform.plugins.LinkedIn").first()
    if (linkedIn_Channel is None):
        print(
            "LinkedIn test failed since the db contains no LinkedIn channel")  # TODO pytest test_ignore ?
    else:
        channel_config = linkedIn_Channel.config
        json_data = json.loads(channel_config)
        pub.channel_id = json_data['id']
        status = linkedin.run(pub, channel_config)
        assert status == "Post successful", "Couldn't post on LinkedIn"


def test_config_sections():
    """
    Test whether the config_parser works
    TODO: to test (yash: i was unable to run the tests)
    """
    config_parser = configparser.ConfigParser()
    config_parser.read('test.ini')
    assert config_parser.sections == ['Credentials', 'Profile_1']


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
        with pytest.raises(FileNotFoundError, args={"message": "A file not found exception was not thrown"}):
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
    file_to_open = data_folder + "/" + ini_file_name
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
