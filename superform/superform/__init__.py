from flask import Flask, render_template, session, request
from superform.auth import auth_page, db as auth_db
from superform.models import User, db as models_db


app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(auth_page)

# Init dbs
auth_db.init_app(app)
models_db.init_app(app)


@app.route('/')
def index():
    user = User.query.get(session.get("id", "")) if session.get("logged_in", False) else None
    return render_template("index.html", user=user)


@app.route('/records')
def records():
    records = [[1,"sub1","body1","FB INGI"],[2,"sub2","body2","Portail ICTEAM"]]
    return render_template('records.html', records = records)


@app.route('/new')
def new_post():
    if request.method == "GET":
        return render_template('new.html')
    else:
        return render_template('done.html')


if __name__ == '__main__':
    app.run()
