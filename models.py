# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
	__tablename__='user'
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))


class History(db.Model):
	__tablename__='history'
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	bmi = db.Column(db.Float())
	id_user = db.Column(db.Integer, db.ForeignKey('user.id'))