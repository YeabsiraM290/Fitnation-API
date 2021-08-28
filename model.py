from enum import *
from operator import le
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

from sqlalchemy.orm import *
from settings import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)


class Users(db.Model):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String,  nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    Timeline = relationship(
        "Timeline", uselist=False, backref="users")
    UserPlan = relationship(
        "UserPlan", uselist=False, backref="users")

    def __init__(self, username, email, password, sex, question, answer):

        self.username = username
        self.email = email
        self.password = password
        self.sex = sex
        self.question = question
        self.answer = answer

    def serialize(self):
        return{

            "username": self.username,
            "email": self.email,
            "age": self.age,
            "sex": self.sex,
            "height": self.height,
            "weight": self.weight
        }


class Admin(db.Model):

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String,  nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):

        self.username = username
        self.email = email
        self.password = password

    def serialize(self):
        return{

            "username": self.username,
            "email": self.email
        }


class Login(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, email, password, role):

        self.email = email
        self.password = password
        self.role = role

    def serialize(self):
        return{

            "role": self.role
        }
 
