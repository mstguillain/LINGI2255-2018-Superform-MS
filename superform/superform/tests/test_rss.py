import datetime
import os
import tempfile
import traceback
import pytest
from linkedin import linkedin
import superform.plugins.rss as rss
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


temp_xml_path = ""
def test_run_rss():
    """
    Checks if a simple linkedin post can be created (require a session being present in the db)
    :return:
    """
    pass


def test_import_items_no_items():
    """
    Test if there no item when creating a new RSS feed
    TODO: create a new xml and get its path
    """
    xml_path = ""
    items = rss.import_items(xml_path)
    assert len(items), "Items were present when it shoudln't have been the case"

def test_import_items_new_items():
    """
    Test if creating a new RSS item  is done properly and doesn't generate double
    TODO: create a new xml and get its path
    """
    xml_path = ""
    items = rss.import_items(xml_path)
    oldlen = len(items)
    items = rss.import_items(xml_path)
    newLen = len(items)
    assert newLen == oldlen + 1, "Addition of one new item to the RSS feed failed"


def test_new_feed():
    pass



def test_get_rss_ini():
    """
    Tests whether the rss.ini file is present in the plugins folder
    """
    pass


