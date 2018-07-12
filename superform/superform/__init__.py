from flask import Flask, render_template, session
from superform.auth import auth_page

app = Flask(__name__)
app.config.from_json("../config.json")
app.register_blueprint(auth_page)


@app.route('/')
def index():
    items = [[1,"sub1","body1"],[2,"sub2","body2"]]
    return render_template("index.html", items=items)

@app.route('/records')
def records():
    records = [[1,"sub1","body1","FB INGI"],[2,"sub2","body2","Portail ICTEAM"]]
    return render_template('records.html', records = records)


if __name__ == '__main__':
    app.run()
