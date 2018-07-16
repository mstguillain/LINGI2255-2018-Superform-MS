from flask import Blueprint, current_app, url_for, request, make_response, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

from superform.utils import login_required

authorizations_page = Blueprint('authorizations', __name__)
db = SQLAlchemy()


@authorizations_page.route("/authorizations")
@login_required()
def authorizations():
    return render_template("authorizations.html")