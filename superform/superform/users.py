from flask import Blueprint, url_for, request, redirect, session, render_template

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, User, Authorization, Channel

posts_page = Blueprint('users', __name__)

def channels_available_for_user(userid):
    chans= []
    auths = db.session.query(Authorization).filter(Authorization.user_id==userid)
    for auth in auths:
        chans.append(db.session.query(Channel).get(auth.channel_id))

    return chans