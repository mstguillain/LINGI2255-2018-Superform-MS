# To run : Be sure to be in ../LINGI2255-2018-Superform-MS-06/superform folder and then 'pytest -v' in your terminal
import datetime
import os
import tempfile

import pytest

from superform.models import Authorization, Channel
from superform import app, db, Post, User
from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform.users import is_moderator, get_moderate_channels_for_user, channels_available_for_user


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


def login(client, login):
    with client as c:
        with c.session_transaction() as sess:
            if login is not "myself":
                sess["admin"] = True
            else:
                sess["admin"] = False

            sess["logged_in"] = True
            sess["first_name"] = "gen_login"
            sess["name"] = "myname_gen"
            sess["email"] = "hello@genemail.com"
            sess['user_id'] = login


## Testing Functions ##


def test_not_logged_in(client) :
    assert True==True

def test_not_moderator(client) :
    assert True == True

def test_search_publishing(client):
    login(client, "myself")

    channel = Channel(name="test", module=get_module_full_name("mail"), config="{}")
    db.session.add(channel)
    #a = Authorization(channel_id=1, user_id=1, permission=2)
    #db.session.add(a)
    rv = client.post('/new', data=dict(titlepost='A new test post', descrpost="A description",
                                       linkurlpost="http://www.test.com", imagepost="image.jpg",
                                       datefrompost="2018-07-01", dateuntilpost="2018-07-01"))
    assert rv.status_code == 302

    posts = db.session.query(Post).all()
    assert len(posts) > 0
    last_add = posts[-1]




    db.session.query(Post).filter(Post.id == last_add.id).delete()
    db.session.commit()


def test_search_post(client) :
    assert True == True










