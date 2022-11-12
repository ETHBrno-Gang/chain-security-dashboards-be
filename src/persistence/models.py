import sqlalchemy
from . import db
from sqlalchemy_serializer import SerializerMixin


class NakamotoCoefficient(db.Model, SerializerMixin):
    __abstract__ = True
    serialize_only = ('date', 'value')

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)


class BitcoinNakamotoCoefficient(NakamotoCoefficient):
    pass

