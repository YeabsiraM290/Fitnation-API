from operator import ne
from os import name
from typing import ClassVar
import datetime as dt

from flask.json import JSONEncoder
from decorators import *
import bcrypt
from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from settings import *
from helpers import *
from model import *
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = SECERET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
db.init_app(app)
CORS(app)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
db.init_app(app)
CORS(app)
class User(Resource):

    def get(self):

        # update_diet_header = request.headers
        user_id = 1 

        userInfo = Users.query.filter(
            Users.user_id == user_id).first()

        if userInfo:

            return userInfo.serialize(), 200

        return 'no user found', 404
    def post(self):

        new_user_info = json.loads(request.form['content'])

        username = new_user_info['username']
        email = new_user_info['email']
        password = new_user_info['password']
        sex = new_user_info['sex']
        age = new_user_info['age']
        question = new_user_info['question']
        answer = new_user_info['answer']
        height = new_user_info['height']
        weight = new_user_info['weight']

        if checkLen(username, 4):

            if isUsernameUnique(username):

                if valEmail(email):

                    if isEmailUnique(email):

                        if checkLen(password, 8):

                            if isBetween(age, 15, 75):

                                if isBetween(height, 1.45, 2.5):

                                    if isBetween(weight, 25, 200):

                                        new_user = Users(
                                            username, email, password, sex, age, height, weight, question, answer)
                                        new_user_credentials = Login(
                                            email, password, "user")

                                        db.session.add(new_user)
                                        db.session.commit()

                                        db.session.add(new_user_credentials)
                                        db.session.commit()

                                        return "Success", 200

                                    else:
                                        return "invalid weight", 401

                                else:
                                    return "invalid height", 401

                            else:
                                return "invalid age", 401

                        else:
                            return "short password", 401

                    else:
                        return "email taken", 401

                else:
                    return "invalid email", 401

            else:
                return "username taken", 401

        return "short username", 401
    def put(self):

        update_diet_header = request.headers
        # user_id = update_diet_header['id']
        user_id = 1

        user = Users.query.filter(
            Users.user_id == int(user_id)).first()

        if user:

            updated_user_info = request.get_json()

            username = updated_user_info['username']
            print(username)
            age = updated_user_info['age']
            height = updated_user_info['height']
            weight = updated_user_info['weight']

            if checkLen(username, 4):

                if isUsernameUnique(username):

                    if isBetween(age, 15, 75):

                        if isBetween(height, 1.45, 2.5):

                            if isBetween(weight, 25, 200):

                                user.username = username
                                user.age = age
                                user.height = height
                                user.weight = weight

                                db.session.add(user)
                                db.session.commit()

                                return "Success", 200

                            else:
                                return "invalid weight", 401

                        else:
                            return "invalid height", 401

                    else:
                        return "invalid age", 401

                else:
                    return "username taken", 401
            else:
                return "short username", 401

        return 'User not found', 404
    def delete(self):

        update_diet_header = request.headers
        # user_id = update_diet_header['id']
        user_id =1

        user = Users.query.filter(
            Users.user_id == int(user_id)).first()

        if user:

            db.session.delete(user)
            db.session.commit()

            return "Success", 200

        return "user doesnot exist", 401
class UpdatePassword(Resource):

    method_decorators = [token_required]

    def put(self, current_user):

        try:

            user_id = current_user.user_id

            user = Users.query.filter(
                Users.user_id == user_id).first()

            if user:

                update_password_body = request.authorization

                password = update_password_body.password
                password_form_request = password.encode(
                    "utf-8")
                password = bcrypt.hashpw(
                    password_form_request, bcrypt.gensalt())

                isValid = checkLen(password, 8)

                if isValid:

                    update_user_credentials = LoginInfo.query.filter(
                        LoginInfo.email == user.email).first()

                    update_user_credentials.password = password

                    db.session.add(update_user_credentials)
                    db.session.commit()

                    return "Success", 200

                return "short password", 401

            return 'User not found', 404

        except Exception as e:

            return e, 401

api.add_resource(UpdatePassword, '/api/updatePassword/')
api.add_resource(User, '/api/user/')

if __name__ == "__main__":
    app.run(debug=True) 
