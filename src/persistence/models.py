from . import db


class Dummy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(31), unique=True, nullable=True)
