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

class RevokeUser(Resource):
    method_decorators = [admin_required]

    def put(self):

        try:
            reovoked_user_header = request.authorization
            user_email = reovoked_user_header.username

            user = Users.query.filter(
                Users.email == user_email).first()

            if user:

                deleted_user_credentials = LoginInfo.query.filter(
                    LoginInfo.email == user_email).first()

                db.session.delete(deleted_user_credentials)
                db.session.commit()

                return "Success", 200

            return 'User not found', 404

        except:
            return 'Server error', 401


class AllowUser(Resource):
    method_decorators = [admin_required]

    def put(self):

        try:
            allowed_user_header = request.authorization
            user_email = allowed_user_header.username

            user = Users.query.filter(
                Users.email == user_email).first()

            if user:

                email = user.email
                password = user.password
                allowed_user_credentials = LoginInfo(email, password, "user")

                db.session.add(allowed_user_credentials)
                db.session.commit()

                return "Success", 200

            return 'User not found', 404

        except:
            return 'Server error', 402


class AddAdmin(Resource):
    method_decorators = [admin_required]

    def post(self):

        try:
            new_admin_header = request.authorization
            email = new_admin_header.username
            password = new_admin_header.password
            password_form_request = password.encode(
                "utf-8")
            password = bcrypt.hashpw(
                password_form_request, bcrypt.gensalt())

            admin = Admin.query.filter(
                Admin.email == email).first()

            if admin:

                return 'Admin already exists', 401

            new_admin_credential = LoginInfo(email, password, "admin")

            db.session.add(new_admin_credential)
            db.session.commit()

            new_admin = Admin(email, password)

            db.session.add(new_admin)
            db.session.commit()

            return "Success", 200

        except:
            return 'Server error', 402


class GeneralReport(Resource):

    method_decorators = [admin_required]

    def get(self):

        try:
            data = {}

            users = Users.query.all()
            users_count = len(users)

            exercises = Exerciseplan.query.all()
            exercises_count = len(exercises)

            data['user_count'] = users_count
            data['exercise_count'] = exercises_count

            return data, 200

        except:
            return 'Server error', 401

class Login(Resource):

    def get(self):

        try:

            login_info = request.authorization
            email = login_info.username
            password = login_info.password

            user = LoginInfo.query.filter(LoginInfo.email == email).first()
            data = {}
            if user:

                if bcrypt.checkpw(password.encode("utf-8"), user.password):
                    print('xxxxxxxxxxxxxx')

                    token = jwt.encode({'email': user.email, 'exp': dt.datetime.utcnow(
                    ) + dt.timedelta(days=30)}, SECERET_KEY)
                    data["token"] = token
                    data["role"] = user.role

                    return data, 200

                return "Email or password not correct.", 401
            else:
                return "user not found or blocked", 404
        except Exception as e:

            return e, 401


class Signup(Resource):

    def post(self):

        try:

            new_user_info = request.get_json()
            userCredientals_info = request.authorization

            username = new_user_info['username']
            email = userCredientals_info.username
            password = userCredientals_info.password
            sex = new_user_info['sex']
            age = new_user_info['age']
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

                                            password_form_request = password.encode(
                                                "utf-8")
                                            password = bcrypt.hashpw(
                                                password_form_request, bcrypt.gensalt())

                                            new_user = Users(
                                                username, email, password, sex, age, height, weight)

                                            db.session.add(new_user)
                                            db.session.commit()

                                            new_user_credentials = LoginInfo(
                                                email, password, 'user')

                                            db.session.add(
                                                new_user_credentials)
                                            db.session.commit()

                                            token = jwt.encode({'email': email, 'exp': dt.datetime.utcnow(
                                            ) + dt.timedelta(days=30)}, SECERET_KEY)

                                            data = {}
                                            data["token"] = token
                                            print("YYYYYY")
                                            data["role"] = "user"

                                            return data, 200

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

        except Exception as e:

            return e, 401


class CheckUserAuthenticity(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        try:
            user = LoginInfo.query.filter(
                LoginInfo.email == current_user.email).first()
            role = user.role

            return {'role': role.lower()}, 200
        except:
            return 'Server error', 401
class ResetPassword(Resource):

    def put(self):

        try:

            update_password_header = request.authorization
            email = update_password_header.username

            user = Users.query.filter(
                Users.email == email).first()

            if user:

                password = update_password_header.password

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

        except:

            return 'Server error', 401
class UserStatus(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        user_id = current_user.user_id

        user = Users.query.filter(Users.user_id == user_id).first()

        user_status = {}

        if user:

            height = user.height
            weight = user.weight
            age = user.age

            bmi = calBMI(height, weight)
            fat = calFat(age, bmi)
            cal = calCalorieIntake(age)

            user_status['bmi'] = bmi
            user_status['fat'] = fat
            user_status['calorie'] = cal
            user_status['weight'] = weight

            userPlan = UserPlan.query.filter(
                UserPlan.user_id == user_id).first()

            if userPlan:

                plan_id = getPlanId(user_id)
                planName = getPlanName(plan_id)
                level = getLevel(user_id)
                goal = getPlanGoal(user_id)

                updateWeek(user_id)
                week = getWeek(user_id)

                user_status['planName'] = planName
                user_status['level'] = level
                user_status['week'] = week
                user_status['goal'] = goal

            user_status['planName'] = "_____"
            user_status['level'] = "_____"
            user_status['week'] = "_____"
            user_status['goal'] = "_____"

            return user_status, 200

        return 'User not found', 404

class DietPlan(Resource):

    method_decorators = [admin_required]

    def get(self):

        try:
            diet_db = Diet.query.all()

            diets = []
            for diet in diet_db:

                diets.append(diet.serialize())

            return diets,  200

        except:
            return 'Server error', 401
def post(self):

        try:
            new_diet_body = request.get_json()

            checkDiet = Diet.query.filter(
                Diet.name == new_diet_body['name']).first()

            if checkDiet:

                return 'Diet already exist', 401

            diet_name = new_diet_body['name']
            monday = json.dumps(new_diet_body['monday'])
            tuesday = json.dumps(new_diet_body['tuesday'])
            wednesday = json.dumps(new_diet_body['wednesday'])
            thursday = json.dumps(new_diet_body['thursday'])
            friday = json.dumps(new_diet_body['friday'])
            saturday = json.dumps(new_diet_body['saturday'])
            sunday = json.dumps(new_diet_body['sunday'])

            new_diet = Diet(diet_name, monday, tuesday, wednesday,
                            thursday, friday, saturday, sunday)

            db.session.add(new_diet)
            db.session.commit()

            return 'success', 200

        except:
            return "Server error", 401

def put(self):

        try:
            update_diet_body = request.get_json()

            checkDiet = Diet.query.filter(
                Diet.name == update_diet_body['name']).first()

            if checkDiet:

                checkDiet.name = update_diet_body['name']
                checkDiet.monday = json.dumps(update_diet_body['monday'])
                checkDiet.tuesday = json.dumps(update_diet_body['tuesday'])
                checkDiet.wednesday = json.dumps(update_diet_body['wednesday'])
                checkDiet.thursday = json.dumps(update_diet_body['thursday'])
                checkDiet.friday = json.dumps(update_diet_body['friday'])
                checkDiet.saturday = json.dumps(update_diet_body['saturday'])
                checkDiet.sunday = json.dumps(update_diet_body['sunday'])

                db.session.add(checkDiet)
                db.session.commit()

                return 'success', 200

            return 'No diet found', 404

        except:
            return 'Server error', 401
api.add_resource(CheckUserAuthenticity, '/api/isUser/')
api.add_resource(Login, '/api/login/')
api.add_resource(Signup, '/api/signup/')
api.add_resource(ResetPassword, '/api/forgetPassword/')
api.add_resource(RevokeUser, '/api/revokeUser/')
api.add_resource(AllowUser, '/api/allowUser/')
api.add_resource(AddAdmin, '/api/newAdmin/')
api.add_resource(GeneralReport, '/api/report')
api.add_resource(UpdatePassword, '/api/updatePassword/')
api.add_resource(User, '/api/user/')

if __name__ == "__main__":
    app.run(debug=True) 
