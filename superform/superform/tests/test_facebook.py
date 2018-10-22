from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel


import sys
sys.path.append("..")
from plugins.facebook_plugin import *
import unittest


class TestStringMethods(unittest.TestCase):

    def test_db(self):

        msg = 'Ceci est une publication de test pour db !'
        cfg = {
            "page_id"      : "285844238930581",  # Step 1
            "access_token" : "EAAHcEGT1yyEBAMMmOCYrWGJAfJZCmlZAxlTc4hDNQ6HrW0r5Od65KrHDsAU2IzCWp2IqTp8JPXwgkbU3DvHRwfTj6j8uZBI4w4pvD0Lrma1cOE2oVTUm3PST9qpGzR2sgB6n8yCshzUSbDBbZA0hROfafsLRZB3M4XwDfoVrOOSS6SGZALizRriZBkZAsI2prtXf9jmVWiZCa3t5pl6DhLV2v"   # Step 3
        }
        api = get_api(cfg)
        publication_id = publish(api, msg)
        print('Publication id : {}'.format(publication_id))
        pub = api.get_object(id=publication_id, fields='message')
        print('Publication : {}'.format(pub))
        idc = db.session.query(Channel).filter(Channel.channel_id=='Facebook')
        publ = db.session.query(Publishing).filter(Publishing.post_id==publication_id,Publishing.channel_id==idc).first()
        print('publ : {}'.format(publ))

    def test_publish(self):
        msg = 'Ceci est une publication !'
        cfg = {
            "page_id"      : "285844238930581",  # Step 1
            "access_token" : "EAAHcEGT1yyEBAMMmOCYrWGJAfJZCmlZAxlTc4hDNQ6HrW0r5Od65KrHDsAU2IzCWp2IqTp8JPXwgkbU3DvHRwfTj6j8uZBI4w4pvD0Lrma1cOE2oVTUm3PST9qpGzR2sgB6n8yCshzUSbDBbZA0hROfafsLRZB3M4XwDfoVrOOSS6SGZALizRriZBkZAsI2prtXf9jmVWiZCa3t5pl6DhLV2v"   # Step 3
        }

        api = get_api(cfg)
        publication_id = publish(api, msg)
        print('Publication id : {}'.format(publication_id))
        pub = api.get_object(id=publication_id, fields='message')
        print('Publication : {}'.format(pub))
        delete(api, publication_id)
        self.assertEquals(msg, pub['message'])

if __name__ == '__main__':
    unittest.main()
