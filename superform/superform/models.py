from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    uid = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    sn = db.Column(db.String(120), nullable=False)
    givenName = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.uid
