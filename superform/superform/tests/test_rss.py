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


def test_run_rss():
    """
    Checks if a simple linkedin post can be created (require a session being present in the db)
    :return:
    """
    pass


def test_import_items():
    pass


def test_new_feed():
    pass



def test_get_rss_ini():
    """
    Tests whether the rss.ini file is present in the plugins folder
    """
    data_folder = Path("superform/plugins")
    file_to_open = data_folder / "rss.ini"
    assert data_folder.is_dir()
    assert file_to_open.is_file()


def test_get_client_id_and_secret():
    """
    Tests whether we find the right values in the test.ini file
    TODO: to test (yash: i was unable to run the tests)
    """
    config = configparser.ConfigParser()
    config.read('test.ini')
    c_id = config.get('Credentials', 'CLIENT_ID')
    c_secret = config.get('Credentials', 'CLIENT_SECRET')
    myhobby = config.get('Profile_1', 'hobby')
    assert c_id == "myclientID"
    assert c_secret == "myclientsecret"
    assert myhobby == 'bass'
