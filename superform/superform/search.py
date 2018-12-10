from flask import Blueprint, url_for, request, session

from superform.utils import login_required
from superform.models import db, Publishing, User, Post
from superform.users import is_moderator, get_moderate_channels_for_user

search_page = Blueprint('search', __name__)

@search_page.route('/search_publishings', methods=['POST'])
@login_required()
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


@search_page.route('/search_post', methods=['POST'])
@login_required()
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