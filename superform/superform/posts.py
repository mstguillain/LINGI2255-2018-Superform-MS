from flask import Blueprint, url_for, request, redirect, session, render_template

import users
from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Post

posts_page = Blueprint('posts', __name__)

@posts_page.route('/new', methods=['GET','POST'])
@login_required()
def new_post():
    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    list_of_channels = users.channels_available_for_user(user_id)
    if request.method == "GET":
        return render_template('new.html', l_chan = list_of_channels)
    else:
        on_channel_post = []

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

@posts_page.route('/edit_post/<int:id>', methods=['GET','POST'])
@login_required()
def edit_post(id):
    p = db.session.query(Post).get(id)

    if request.method == "GET":
        p.date_from = str_converter(p.date_from)
        p.date_until = str_converter(p.date_until)
        return render_template("edit_post.html",post = p)
    elif request.method == "POST":
        p.title = request.form.get('titlepost')
        p.description = request.form.get('descrpost')
        p.link_url = request.form.get('linkurlpost')
        p.image_url = request.form.get('imagepost')
        p.date_from = datetime_converter(request.form.get('datefrompost'))
        p.date_until = datetime_converter(request.form.get('dateuntilpost'))
        return redirect(url_for('index'))


@posts_page.route('/delete_post/<int:id>')
@login_required()
def delete_post(id):
    db.session.query(Post).filter(Post.id==id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@posts_page.route('/records')
@login_required()
def records():
    posts = db.session.query(Post).filter(Post.user_id==session.get("user_id", ""))
    records = [(p) for p in posts if is_a_record(p.id)]
    return render_template('records.html', records=records)


def is_a_record(pid):
    post = db.session.query(Post).get(pid)
    if (len(post.publishings)==0):
        return False
    else:
        for pub in post.publishings:
            if(pub.state != 2):
                #TODO change value. ftm state 2 is published.
                return False
        return True



