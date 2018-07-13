from flask import Flask, render_template, session, request, redirect, url_for

from superform.models import User,Channel, db as models_db
from superform.authentication import authentication_page, db as authentication_db
from superform.authorizations import authorizations_page, db as authorizations_db
from superform.utils import login_required


app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)

# Init dbs
authentication_db.init_app(app)
models_db.init_app(app)
authorizations_db.init_app(app)

@app.route('/')
def index():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    return render_template("index.html", user=user)


@app.route('/records')
def records():
    records = [[1,"sub1","body1","FB INGI"],[2,"sub2","body2","Portail ICTEAM"]]
    return render_template('records.html', records = records)


@app.route('/new')
@login_required()
def new_post():
    if request.method == "GET":
        return render_template('new.html')
    else:
        return render_template('done.html')

@app.route('/new_channel', methods=['GET','POST'])
@login_required
def new_channel():
    if request.method == "GET":
        return render_template('new_channel.html',pluginparams={})
    elif request.method == "POST":
        channelname = request.form.get('chanName')
        c = Channel(name=channelname,module="mail",config={})
        models_db.session.add(c)
        models_db.commit()
        return redirect(url_for('index'))





@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
