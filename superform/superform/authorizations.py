from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required
from superform.models import db, Channel, Authorization, Permission

authorizations_page = Blueprint('authorizations', __name__)


@authorizations_page.route("/authorizations")
@login_required()
def authorizations():
    if session["admin"]:
        channels = Channel.query.all()
    else:
        channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"])

    return render_template("authorizations.html", channels=channels, permissions=Permission)