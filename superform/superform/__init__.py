from flask import Flask, render_template, session, request, redirect, url_for
import pkgutil
import importlib

import superform.plugins
from superform.models import db, User, Channel
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.utils import login_required

app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)
app.register_blueprint(channels_page)

# Init dbs
db.init_app(app)

# List available channels in config
app.config["PLUGINS"] = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
}


@app.route('/')
def index():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    return render_template("index.html", user=user)


@app.route('/records')
def records():
    records = [[1, "sub1", "body1", "FB INGI"], [2, "sub2", "body2", "Portail ICTEAM"]]
    return render_template('records.html', records=records)


@app.route('/new')
@login_required()
def new_post():
    if request.method == "GET":
        return render_template('new.html')
    else:
        return redirect(url_for('index'))


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
