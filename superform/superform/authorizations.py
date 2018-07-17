from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required
from superform.models import db, Channel, Authorization, Permission

authorizations_page = Blueprint('authorizations', __name__)


@authorizations_page.route("/authorizations")
@login_required()
def authorizations():
    if session["admin"]:
        rw_channels = Channel.query.all()
        ro_channels = []
    else:
        channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"])
        rw_channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"]).filter(Authorization.permission == Permission.MODERATOR.value)
        ro_channels = Channel.query.join(Authorization).filter(Authorization.user_id == session["user_id"]).filter(Authorization.permission == Permission.AUTHOR.value)

    return render_template("authorizations.html", rw_channels=rw_channels, ro_channels=ro_channels, permissions=Permission)