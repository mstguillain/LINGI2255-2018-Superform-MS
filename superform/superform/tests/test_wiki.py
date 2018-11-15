# import os
# import sys
# import tempfile
# import datetime
# import string
# import random
# from twitter import twitter_utils
#
# #import pytest
#
# from superform import app, db, Publishing, channels
# from superform.models import Channel, db
# from superform.plugins import wiki
#
#
# FIELDS_UNAVAILABLE = []
# CONFIG_FIELDS = ["username","password"]
#
#
# #Test de la fonction qui decoupe un publishing et la mets dans le bon format
# def test_makeText():
#     pub = Publishing()
#     pub.user_id= "me myself and I"
#     pub.post_id="1"
#     pub.date_from='13.02.02'
#     pub.title='test-Title'
#     pub.link_url = 'blablablablablablablajdsfvjdbvjdnfvqebdnbqdfnvsdùnvbmqknkfnbùsfvdf'
#     pub.description = 'descr'
#     pub.image_url = 'image url'
#     pub.date_until = '14.02.16'
#     pub.state = 1
#     pub.channel_id='wiki'
#
#     text = wiki.makeText(pub)
#     tab_of_text=text.splitlines()
#     date = str(datetime.datetime.now().strftime("%d/%m/%Y"))
#
#     assert tab_of_text[0]=="!! " + pub.title
#     assert tab_of_text[1] == "-----" + "Par " + "Superform" + " Publie le " + date
#     assert tab_of_text[2]==  str(pub.description).replace("\n","[[<<]]")
#     assert tab_of_text[3]== "-----"+"[["+pub.link_url+"]]"
#
#
#
#
