from flask import Flask, render_template, session
from superform.auth import auth_page

app = Flask(__name__)
app.config.from_json("../config.json")
app.register_blueprint(auth_page)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/records')
def records():
    return render_template('records.html')


if __name__ == '__main__':
    app.run()
