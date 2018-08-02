from flask import Blueprint, url_for, request, redirect, session, render_template

from superform.users import channels_available_for_user
from superform.utils import login_required, datetime_converter, str_converter, get_instance_from_module_path
from superform.models import db, Post, Publishing

posts_page = Blueprint('posts', __name__)

def create_a_post(form):
    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    title_post = form.get('titlepost')
    descr_post = form.get('descriptionpost')
    link_post = form.get('linkurlpost')
    image_post =form.get('imagepost')
    date_from = datetime_converter(form.get('datefrompost'))
    date_until = datetime_converter(form.get('dateuntilpost'))
    p= Post(user_id=user_id, title=title_post, description=descr_post, link_url=link_post, image_url=image_post,
             date_from=date_from, date_until=date_until)
    db.session.add(p)
    db.session.commit()
    return p


@posts_page.route('/new', methods=['GET','POST'])
@login_required()
def new_post():
    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    list_of_channels = channels_available_for_user(user_id)
    for elem in list_of_channels:
        m = elem.module
        clas = get_instance_from_module_path(m)
        unaivalable_fields = ','.join(clas.FIELDS_UNAVAILABLE)
        setattr(elem,"unavailablefields",unaivalable_fields)

    if request.method == "GET":
        return render_template('new.html', l_chan = list_of_channels)
    else:
        create_a_post(request.form)
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

@posts_page.route('/publish', methods= ['POST'])
@login_required()
def publish_from_new_post():
    #First create the post
    p = create_a_post(request.form)
    #then treat the publish part
    if request.method=="POST":
        for elem in request.form:
            if elem.startswith("chan_option_"):
                #for each selected channel options
                #create the publication
                pub = Publishing(post_id=p.id,channel_id=request.form.get(elem),state=0)
                db.session.add(pub)

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



