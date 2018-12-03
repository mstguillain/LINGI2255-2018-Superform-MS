from flask import Flask, render_template, session
#For search
from flask import request, url_for
import json
#
import pkgutil
import importlib

import superform.plugins
from superform.publishings import pub_page
from superform.models import db, User, Post,Publishing
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.posts import posts_page
from superform.users import get_moderate_channels_for_user, is_moderator

app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)
app.register_blueprint(channels_page)
app.register_blueprint(posts_page)
app.register_blueprint(pub_page)

# Init dbs
db.init_app(app)

# List available channels in config
app.config["PLUGINS"] = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
}

@app.route('/search_publishings', methods=['POST'])
def search_publishings() :
    data =''
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    posts = []
    chans = []
    flattened_list_pubs = []
    if user is not None:
        setattr(user, 'is_mod', is_moderator(user))
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.name) &
                                                             (Publishing.title.like('%'+request.form['subject']+'%')) &
                                                             (Publishing.description.like('%' + request.form['body'] + '%')) &
                                                             (Publishing.state == 0)) for c in chans)
        flattened_list_pubs = [y for x in pubs_per_chan for y in x]
        data = '['
        i = 0
        for p in flattened_list_pubs :
            if request.form['author'] in p.get_author() and p.channel_id in request.form.getlist('channels[]'):
                if i != 0 :
                    data += ','
                data += '{"channel": "'+p.channel_id+'" , "subject" : "'+p.title+'", "body":"'+str(p.description.splitlines()) +'", "author":"'+p.get_author()+'",'
                data += '"button":"'+ url_for('publishings.moderate_publishing',id=p.post_id,idc=p.channel_id)+'"}'
                i = i + 1
        data += ']'
    return str(data)

@app.route('/search_post', methods=['POST'])
def search_post() :
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    posts=[]
    data = '[]'
    if user is not None:
        setattr(user,'is_mod',is_moderator(user))
        posts = db.session.query(Post).filter((Post.user_id==session.get("user_id", "")) &
                                              (Post.title.like('%'+request.form['subject']+'%')) &
                                              (Post.description.like('%'+request.form['body']+'%'))
                                              ).order_by(request.form['sorted'])

        data = '['
        i = 0
        for item in posts :

            if i != 0 :
                data += ','

            data += '{ "id":"'+str(item.id)+'", "title":"'+ item.title +'", "description" : "'+ str(item.description.splitlines())+'",'
            #For buttons in this table, add url there
            data += '"hrefEdit" : "#", "hrefCopy" : "#", "hrefDelete" : "#" }'
            i = i + 1
        data += ']'
    return str(data)

@app.route('/')
def index():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    posts=[]
    flattened_list_pubs =[]
    chans = []
    if user is not None:
        setattr(user,'is_mod',is_moderator(user))
        posts = db.session.query(Post).filter(Post.user_id==session.get("user_id", ""))
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.name) & (Publishing.state == 0)) for c in chans)
        flattened_list_pubs = [y for x in pubs_per_chan for y in x]

    return render_template("index.html", user=user,posts=posts,publishings = flattened_list_pubs, channels = chans)

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
