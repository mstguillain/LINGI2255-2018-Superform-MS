from datetime import datetime

from flask import Flask, render_template, session, request, redirect, url_for
import pkgutil
import importlib

from sqlalchemy import func

import superform.plugins
from superform.models import db, User, Channel, Post
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.utils import login_required

app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)
app.register_blueprint(channels_page)

# Init dbs
db.init_app(app)

# List available channels in config
app.config["PLUGINS"] = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
}


@app.route('/')
def index():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    posts = db.session.query(Post).filter(Post.user_id==session.get("user_id", "") and func.count(Post.publishings)== 0)
    return render_template("index.html", user=user,posts=posts)


@app.route('/records')
@login_required()
def records():
    records = [[1, "sub1", "body1", "FB INGI"], [2, "sub2", "body2", "Portail ICTEAM"]]
    return render_template('records.html', records=records)


@app.route('/new', methods=['GET','POST'])
@login_required()
def new_post():
    list_of_channels = []
    if request.method == "GET":
        return render_template('new.html')
    else:
        on_channel_post = []

        def datetime_converter(str):
            return datetime.strptime(str,"%Y-%m-%d")
        user_id=session.get("user_id", "") if session.get("logged_in", False) else -1
        title_post = request.form.get('titlepost')
        descr_post = request.form.get('descrpost')
        link_post = request.form.get('linkurlpost')
        image_post = request.form.get('imagepost')
        date_from = datetime_converter(request.form.get('datefrompost'))
        date_until = datetime_converter(request.form.get('dateuntilpost'))
        for chan in list_of_channels:
            if(request.form.get(chan) is True):
                on_channel_post.append(chan)

        p = Post(user_id=user_id,title=title_post,description=descr_post,link_url=link_post,image_url=image_post,date_from=date_from,date_until=date_until)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/delete_post/<int:id>')
@login_required()
def delete_post(id):
    db.session.query(Post).filter(Post.id==id).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
