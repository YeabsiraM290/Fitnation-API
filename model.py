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
class Exerciseplan(db.Model):

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    pic = db.Column(db.String, nullable=False)
    schedule = db.Column(db.String, nullable=False)
    Timeline = relationship(
        "Timeline", uselist=False, backref="exercisePlan")
    UserPlan = relationship(
        "UserPlan", uselist=False, backref="exerciseplan")

    def __init__(self, name, pic, schedule):

        self.name = name
        self.pic = pic
        self.schedule = schedule

    def serialize(self):

        return{

            "name": self.name,
            "pic": self.pic,
            "schedule": json.loads(self.schedule)

        }


class Diet(db.Model):

    diet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    schedule = db.Column(db.String, nullable=False)

    def __init__(self, name, schedule):

        self.name = name
        self.schedule = schedule

    def serialize(self):

        return{

            "name": self.name,
            "schedule": json.loads(self.schedule)

        }


class Timeline(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        'exerciseplan.plan_id'), nullable=False)
    exercise = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)

    def __init__(self, date, day, user_id, plan_id, exercise, status, level):

        self.date = date
        self.day = day
        self.user_id = user_id
        self.plan_id = plan_id
        self.exercise = exercise
        self.status = status
        self.level = level

    def serialize(self):

        return{

            "date": self.date,
            "day": self.day,
            "exercise": json.loads(self.exercise),
            "status": self.status

        }


class UserPlan(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        'exerciseplan.plan_id'), nullable=False)
    level = db.Column(db.String, nullable=False)
    week = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, plan_id, level, week):

        self.user_id = user_id
        self.plan_id = plan_id
        self.level = level
        self.week = week

    def serialize(self):

        return{

            "level": self.level,
            "week": self.week
        }


def create():

    db.drop_all()
    db.create_all()
 
