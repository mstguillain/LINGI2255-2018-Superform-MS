# To run : Be sure to be in Superform/superform folder and then 'pytest -v' in your terminal
import datetime
import os
import tempfile

import pytest

from superform import app, db, Post, datetime_converter, str_converter


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


def test_index_not_logged_in(client):
    rv = client.get('/', follow_redirects=True)
    assert rv.status_code == 200
    assert "Your are not logged in." in rv.data.decode()


def test_other_pages_not_logged_in(client):
    rv = client.get('/records', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    rv = client.get('/new', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    rv = client.get('/edit_post/1', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    rv = client.get('/delete_post/1', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    rv = client.get('/channels', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()


def test_index_logged_in(client):
    login(client, "myself")
    rv2 = client.get('/', follow_redirects=True)
    assert rv2.status_code == 200
    assert "Your are not logged in." not in rv2.data.decode()

def test_new_post(client):
    login(client,"myself")
    rv = client.post('/new',data=dict(titlepost='A new test post', descrpost= "A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    assert rv.status_code ==302
    posts = db.session.query(Post).all()
    assert len(posts)>0
    last_add = posts[-1]
    assert last_add.title == 'A new test post'
    db.session.query(Post).filter(Post.id == last_add.id).delete()
    db.session.commit()
    
def test_edit_post(client):
    login(client, "myself")
    rv = client.post('/new', data=dict(titlepost='A new test post', descrpost="A description",
                                       linkurlpost="http://www.test.com", imagepost="image.jpg",
                                       datefrompost="2018-07-01", dateuntilpost="2018-07-01"))
    assert rv.status_code == 302
    post = db.session.query(Post).all()[-1]
    newtitle = "aaaa"
    assert post.title != newtitle
    rv = client.post('/edit_post/'+str(post.id), data=dict(titlepost=newtitle, descrpost="A description",
                                       linkurlpost="http://www.test.com", imagepost="image.jpg",
                                       datefrompost="2018-07-01", dateuntilpost="2018-07-01"))

    assert rv.status_code == 302
    assert post.title == newtitle
    db.session.query(Post).filter(Post.id == post.id).delete()
    db.session.commit()

def test_delete_post(client):
    login(client, "myself")
    rv = client.post('/new', data=dict(titlepost='A new test post', descrpost="A description",
                                       linkurlpost="http://www.test.com", imagepost="image.jpg",
                                       datefrompost="2018-07-01", dateuntilpost="2018-07-01"))
    assert rv.status_code == 302
    posts = db.session.query(Post).all()
    size_posts = len(posts)
    post = posts[-1]
    rv = client.get('/delete_post/'+str(post.id))
    assert rv.status_code ==302
    posts = db.session.query(Post).all()
    assert len(posts) == size_posts-1
    assert db.session.query(Post).get(post.id) is None
    
def test_not_found(client):
    login(client,"myself")
    rv = client.get('/unknownpage')
    assert rv.status_code == 404
    assert "Page not found" in rv.data.decode()


def test_forbidden(client):
    # Not connected
    rv = client.get('/channels', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    # myself is not admin
    login(client, "myself")
    rv = client.get('/channels', follow_redirects=True)
    assert rv.status_code == 403
    assert "Forbidden" in rv.data.decode()
    # an_admin is admin
    login(client, "an_admin")
    rv = client.get('/channels', follow_redirects=True)
    assert rv.status_code == 200
    assert "Forbidden" not in rv.data.decode()

def test_date_converters():
    t = datetime_converter("2017-06-02")
    assert t.day == 2
    assert t.month == 6
    assert t.year == 2017
    assert isinstance(t, datetime.datetime)
    st = str_converter(t)
    assert isinstance(st,str)


    



