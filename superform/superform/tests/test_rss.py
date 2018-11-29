import pytest
from flask import current_app, request
import json
import rfeed
import datetime
import os
import feedparser

from rss import rss


def test_run_feed_simple():
    """
    Checks if a simple linkedin post can be created (require a session being present in the db)
    :return:
    """

    rname = "TestField2"
    rdescription = "Trying to create a new field"
    # Creating the new field

    feed, nameOfFeed = rss.newFeed(rname, rdescription)
    expectedNameOfFeed = rname.replace(" ", "_")
    assert feed, "No new feed was created"
    assert nameOfFeed == expectedNameOfFeed, "The name of the field was modified or wrong : expected {} from {}  but got {}".format(
        expectedNameOfFeed, rname, nameOfFeed)
    assert feed.link, "The new feed doesn't have any link"
    assert feed.description == rdescription, "The new feed doesn't have the expected description"

    #   TODO: maybe test the date too ?


def test_run_feed_bad_name():
    """
        Trying to create a new field with no name, should give an error
    :return:
    """

    rname = ""
    rdescription = "Trying to create a new field with no name"

    # TODO : replace ValueError by something more general, we are just expecting an error
    with pytest.raises(ValueError, message="The RSS feed allows us to create a post with no title"):
        feed, nameOfFeed = rss.newFeed(rname, rdescription)


def test_run_feed_bad_description():
    """
        Trying to create a new field with no name, should give an error
    :return:
    """

    rname = "Test feed with no description"
    rdescription = ""

    # TODO : replace ValueError by something more general, we are just expecting an error
    with pytest.raises(ValueError, message="The RSS feed allows us to create a post with no description"):
        feed, nameOfFeed = rss.newFeed(rname, rdescription)


def test_import_items():
    """
        Check if we can properly publish a new feed
    :return:
    """

    rname = "TestField2"
    rdescription = "Trying to create a new field and see if no data was lsot"
    # Creating the new field

    feed, nameOfFeed = rss.newFeed(rname, rdescription)
    assert feed.link, "The new feed doesn't have any link , can't test the created content"
    items = rss.import_items(feed.link)
    found_wanted_feed = False

    for item in items:
        if item.description == rdescription and item.title == rname.replace(" ", "_"):
            found_wanted_feed = True
            print("The new field was well created")
            return
    assert found_wanted_feed, "The new rss publishign failled"

def test_publish_base():
    """
        Trying publishing to an existing RSS Feed
    :return:
    """

    #publishing, channel_config

    #rss.run()
    pass