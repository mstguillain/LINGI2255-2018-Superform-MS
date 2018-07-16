from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template

from superform.utils import login_required
from superform.models import db

authorizations_page = Blueprint('authorizations', __name__)


@authorizations_page.route("/authorizations")
@login_required()
def authorizations():
    return render_template("authorizations.html")