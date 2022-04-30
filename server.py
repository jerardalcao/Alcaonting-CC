from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credit-card.db'
db = SQLAlchemy(app)
query = sqlite3.connect('credit-card.db')
cursor = query.cursor()

class Creditcards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cc_id = db.Column(db.Integer, db.ForeignKey(Creditcards.id), nullable=False)
    cc_alias = db.relationship('Creditcards',backref=db.backref('transactions',lazy=True))
    date = db.Column(db.Date, nullable=False)
    vendor = db.Column(db.String, nullable=False)
    particulars = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user_name = db.relationship('Users', backref=db.backref('transactions', lazy=True))
