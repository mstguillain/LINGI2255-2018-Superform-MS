from flask import Flask, render_template, session
from superform.auth import auth_page

app = Flask(__name__)
app.config.from_json("../config.json")
app.register_blueprint(auth_page)


@app.route('/')
def index():
    attrs = session.get("attrs", {})
    return render_template("index.html",
                           logged_in=session.get("loggedin", False),
                           user_name=str(attrs.get("givenName", "") + " " + attrs.get("sn", "")),
                           attrs=str(attrs))


if __name__ == '__main__':
    app.run()
