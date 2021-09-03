from enum import *
from operator import le
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    Timeline = relationship(
        "Timeline", uselist=False, backref="users")
    UserPlan = relationship(
        "UserPlan", uselist=False, backref="users")

    def __init__(self, username, email, password, sex, age, height, weight):

        self.username = username
        self.email = email
        self.password = password
        self.sex = sex
        self.age = age
        self.height = height
        self.weight = weight

    def serialize(self):
        return{

            "username": self.username,
            "emailAddress": self.email,
            "age": self.age,
            "sex": self.sex,
            "height": self.height,
            "weight": self.weight
        }


class Admin(db.Model):

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):

        self.email = email
        self.password = password

    def serialize(self):
        return{
            "email": self.email
        }


class LoginInfo(db.Model):

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
    beginner = db.Column(db.String, nullable=False)
    intermidate = db.Column(db.String, nullable=False)
    advanced = db.Column(db.String, nullable=False)
    Timeline = relationship(
        "Timeline", uselist=False, backref="exercisePlan")
    UserPlan = relationship(
        "UserPlan", uselist=False, backref="exerciseplan")

    def __init__(self, name, pic, beginner, intermidate, advanced):

        self.name = name
        self.pic = pic
        self.beginner = beginner
        self.intermidate = intermidate
        self.advanced = advanced

    def serialize(self):

        return{

            "name": self.name,
            "pic": self.pic,
            "beginner": json.loads(self.beginner),
            "intermidate": json.loads(self.intermidate),
            "advanced": json.loads(self.advanced)

        }


class Diet(db.Model):

    diet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    monday = db.Column(db.String, nullable=False)
    tuesday = db.Column(db.String, nullable=False)
    wednesday = db.Column(db.String, nullable=False)
    thursday = db.Column(db.String, nullable=False)
    friday = db.Column(db.String, nullable=False)
    saturday = db.Column(db.String, nullable=False)
    sunday = db.Column(db.String, nullable=False)

    def __init__(self, name, monday, tuesday, wednesday, thursday, friday, saturday, sunday):

        self.name = name
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday

    def serialize(self):

        return{

            "name": self.name,
            "monday": json.loads(self.monday),
            "tuesday": json.loads(self.tuesday),
            "wednesday": json.loads(self.wednesday),
            "thursday": json.loads(self.thursday),
            "friday": json.loads(self.friday),
            "saturday": json.loads(self.saturday),
            "sunday": json.loads(self.sunday)

        }


class Timeline(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey(
        'exerciseplan.plan_id'), nullable=False)
    workouts = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    def __init__(self, date, user_id, plan_id, workouts, status):

        self.date = date
        self.user_id = user_id
        self.plan_id = plan_id
        self.workouts = workouts
        self.status = status

    def serialize(self):

        return{

            "date": self.date,
            "workouts": json.loads(self.exercise),
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
