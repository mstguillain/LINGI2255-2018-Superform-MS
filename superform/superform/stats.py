from flask import Blueprint, url_for, request, redirect, session, render_template
from superform.users import channels_available_for_user
from superform.utils import login_required, datetime_converter, str_converter, get_instance_from_module_path
from superform.models import db, Post, Publishing, Channel, User
import facebook
import json
import http
import urllib.request
from .plugins import gcal_plugin

stats_page = Blueprint('stats', __name__)

def stats_channel():
    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    list_of_channels = channels_available_for_user(user_id)
    label = []
    count = []
    for c in list_of_channels:
        label.append(c.name)
        count.append(c.count)
    return {'label' : label, 'count' : count}

def number_of_posts():
    return db.session.query(Post).filter(Post.user_id == session.get("user_id", "")).count()

def number_of_publishings():
    return db.session.query(Publishing).filter(Post.user_id == session.get("user_id", "")).count()

def number_of_accepted():
    return db.session.query(Publishing)\
    .filter(Publishing.user_id == session.get("user_id", ""),\
    Publishing.state == 1).count()

@stats_page.route('/stats')
@login_required()
def stats():
    data = {
        'channels' : stats_channel(),
        'number_of_posts' : number_of_posts(),
        'number_of_publishings' : number_of_publishings(),
        'number_of_accepted' : number_of_accepted()
    }
    return render_template('stats.html', data=data).encode( "utf-8" )
