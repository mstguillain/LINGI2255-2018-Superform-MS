"""
author: Team 06
date: December 2018
Plugin for the PDF feature
"""

from flask import url_for, redirect

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = []


def run(publishing, channel_config):
    """ Gathers the informations in the config column and launches the
    posting process """
    # TODO


def export():
    """
    Launches the export
    :return:
    """
    print("Here is the export method")
    # TODO
    run(publishing = None, channel_config = None)
    return redirect(url_for('index'))


def create_pdf():
    """

    :return:
    """
    print("Here is the create_pdf method")
    # TODO
