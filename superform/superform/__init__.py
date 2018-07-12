from flask import Flask, render_template, session
from superform.auth import auth_page, db as auth_db
from superform.models import User, db as models_db

app = Flask(__name__)
app.config.from_json("../config.json")

# Register blueprints
app.register_blueprint(auth_page)

# Init dbs
auth_db.init_app(app)
models_db.init_app(app)


@app.route('/')
def index():
    user = User.query.get(session["uid"]) if session.get("logged_in", False) else None
    return render_template("index.html", user=user)


if __name__ == '__main__':
    app.run()
