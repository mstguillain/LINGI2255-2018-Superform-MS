import sys
sys.path.append("..")
import unittest
from urllib.request import urlopen
from superform.plugins import facebook_plugin
from superform import app, db, User, Publishing, channels, Post
from superform.models import Channel, db
from superform.tests.test_basic import client, login, write_to_db, create_user, create_channel, create_auth
from superform.utils import get_module_full_name, str_converter
import pytest, random, string, json
import requests
from datetime import datetime, timedelta


def setup_db(channel_name, channel_module):
    facebook_config = {'page_id': '285844238930581'}

    user = create_user(id=10, name="test10", first_name="utilisateur10", email="utilisateur10.test@uclouvain.be")
    facebook_plugin.setToken(json.dumps(facebook_config.page_id))
    channel = create_channel(channel_name, channel_module, facebook_config)

    post = basic_post(user.id)
    write_to_db(post)
    pub = publish_from_post(post, channel_name)
    write_to_db(pub)
    return user, channel, post, pub


def delete_db(user, channel, post, pub):
    db.session.query(User).filter(User.id == user.id).delete()
    db.session.query(Channel).filter(Channel.id == channel.id).delete()
    db.session.query(Post).filter(Post.id == post.id).delete()
    db.session.query(Publishing).filter(Publishing.post_id == post.id,
                                        Publishing.channel_id == channel.name).delete()
    db.session.commit()


def basic_post(user_id, title=None, delta=timedelta(hours=1)):
    post = Post()
    post.user_id = user_id
    post.title = title if title else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    post.description = 'This is a test !'
    post.date_from = datetime.now() + timedelta(days=1)
    post.date_until = post.date_from + delta
    return post


def publish_from_post(post, channel_id):
    pub = Publishing()
    pub.post_id = post.id
    pub.title = post.title
    pub.description = post.description
    pub.date_from = post.date_from
    pub.date_until = post.date_until
    pub.state = 0
    pub.channel_id = channel_id
    return pub


def basic_publish(title=None, delta=timedelta(hours=1)):
    pub = Publishing()
    pub.title = title if title else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    pub.description = 'This is a test !'
    pub.date_from = datetime.now() + timedelta(days=1)
    pub.date_until = pub.date_from + delta
    pub.state = 0
    pub.channel_id = 'facebook_plugin'
    return pub


# tries to publish an event by using the run function of the gcal_plugin and
# then will check if it was actually published by getting the list of all published events.
def test_run_facebook(client):
    user, channel, post, pub = setup_db(channel_name='test_facebook', channel_module='facebook_plugin')
    login(client, user.id)
    rv = client.post('/moderate/' + str(post.id) + '/test_facebook',
                     data=dict(titlepost=pub.title,
                               descrpost=pub.description,
                               linkurlpost=pub.link_url,
                               imagepost=pub.image_url,
                               datefrompost=str_converter(pub.date_from),
                               dateuntilpost=str_converter(pub.date_until)))

    creds = json.loads(user.fb_cred)
    json_data = json.loads(channel)
    CFG = {
        "page_id": "UNDEFINED",  # Step 1
        "access_token": "UNDEFINED"
    }
    if (CFG['page_id'] == "UNDEFINED"):
        CFG['page_id'] = json_data['page_id']

    if (CFG['access_token'] == "UNDEFINED"):
        CFG['access_token'] = facebook_plugin.setToken(CFG['page_id'])  # Check fb_cred in table User for corresponding access_token

    if (CFG['access_token'] == "ACCESS_TOKEN_NOT_FOUND"):
        # May happen in two cases
        # 1) the user has not generated its token yet
        # 2) the user try to publish to a FB page he/she doesn't own

        CFG['access_token'] = facebook_plugin.setToken(CFG['page_id'])
        if (CFG['access_token'] == "ACCESS_TOKEN_NOT_FOUND"):
            print("NO TOKEN FOUND")
        else:
            print("token refreshed after error")
    api = facebook_plugin.get_api(CFG)

    url = 'https://graph.facebook.com/%d/posts/%d/' % (user.id, json_data['page_id'])
    parameters = {'access_token': facebook_plugin.setToken(CFG['page_id'])}
    r = requests.get(url, params=parameters)
    result = json.loads(r.text)
    if result['data'] and result['data']['message']==pub.title+" "+pub.description:
        goal= True
    else:
        print(result)
        goal= False
    assert goal != True


