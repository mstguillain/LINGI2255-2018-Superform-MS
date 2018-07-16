from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

from superform.utils import login_required
from superform.models import Channel

channels_page = Blueprint('channels', __name__)
db = SQLAlchemy()


@channels_page.route("/channels")
@login_required(admin_required=True)
def channels():
    channels = Channel.query.all()
    return render_template("channels.html", channels=channels, modules=current_app.config["PLUGINS"].keys())