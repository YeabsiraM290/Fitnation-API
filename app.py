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

# Admin


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


# User
class Login(Resource):

    def get(self):

        try:

            login_info = request.authorization
            email = login_info.username
            password = login_info.password

            user = LoginInfo.query.filter(LoginInfo.email == email).first()
            data = {}
            if user:

                if password == user.password:

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

                                if isBetween(age, 10, 75):

                                    if isBetween(height, 1.45, 2.5):

                                        if isBetween(weight, 25, 200):

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
                            return "email taken", 402

                    else:
                        return "invalid email", 401

                else:
                    return "username taken", 400

            return "short username", 401

        except Exception as e:

            return 'Server error', 401


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


class UpdatePassword(Resource):

    method_decorators = [token_required]

    def put(self, current_user):

        try:

            user_id = current_user.user_id
            print(current_user.username)

            user = Users.query.filter(
                Users.user_id == int(user_id)).first()

            if user:

                update_password_body = request.authorization

                password = update_password_body.password

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

                    if update_user_credentials:

                        update_user_credentials.password = password

                        db.session.add(update_user_credentials)
                        db.session.commit()

                        return "Success", 200

                    return 'User blocked', 404

                return "short password", 401

            return 'User not found', 404

        except:

            return 'Server error', 401


class UserExercisePlan(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        try:
            user_id = current_user.user_id
            userPlanInfo = UserPlan.query.filter(
                UserPlan.user_id == user_id).first()

            if userPlanInfo:

                level = getLevel(user_id)
                plan_id = userPlanInfo.plan_id

                updateLevel(user_id, plan_id, level)
                updateWeek(user_id)
                level = getLevel(user_id)
                schedule = getWorkouts(plan_id, level)

                return schedule, 200

            return 'no plan found', 404

        except:

            return 'Server error', 401

    def post(self, current_user):

        try:
            user_id = current_user.user_id
            plan_name = request.get_json()['name']

            plan = Exerciseplan.query.filter(
                Exerciseplan.name == plan_name).first()

            if plan:

                new_plan = UserPlan(user_id, plan.plan_id, 'beginner', 1)

                db.session.add(new_plan)
                db.session.commit()

                return "success", 200

            return "plan doesn't exist", 404

        except:

            return 'Server error'

    def delete(self, current_user):

        try:
            user_id = current_user.user_id

            userPlan = UserPlan.query.filter(
                UserPlan.user_id == user_id).first()

            if userPlan:

                db.session.delete(userPlan)
                db.session.commit()

                resetTimeline(user_id)

                return "success", 200

            return "Plan doesnot exist", 401
        except:

            return 'Server error', 401


class User(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        try:
            user_id = current_user.user_id

            userInfo = Users.query.filter(
                Users.user_id == int(user_id)).first()

            if userInfo:

                return userInfo.serialize(), 200

            return 'no user found', 404

        except:
            return 'Server error', 401

    def put(self, current_user):

        try:
            user_id = current_user.user_id

            user = Users.query.filter(
                Users.user_id == int(user_id)).first()

            if user:

                updated_user_info = request.get_json()

                username = updated_user_info['username']
                age = updated_user_info['age']
                height = updated_user_info['height']
                weight = updated_user_info['weight']
                print(username)
                if checkLen(username, 4):

                    if isUsernameUnique(username):

                        if isBetween(age, 10, 80):

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

        except Exception as e:

            return e, 401

    def delete(self, current_user):

        try:

            user_id = current_user.user_id

            user = Users.query.filter(
                Users.user_id == int(user_id)).first()

            if user:

                resetTimeline(user_id)
                delPlan(user_id)

                db.session.delete(user)
                db.session.commit()

                return "Success", 200

            return "user doesn't exist", 404

        except Exception as e:

            return 'Server error', 401


class UserDietPlan(Resource):
    method_decorators = [token_required]

    def get(self, current_user):

        try:
            user_id = current_user.user_id

            userPlanInfo = UserPlan.query.filter(
                UserPlan.user_id == int(user_id)).first()

            if userPlanInfo:

                plan_name = getPlanName(userPlanInfo.plan_id)

                dietInfo = Diet.query.filter(Diet.name == plan_name).first()

                diet_info = dietInfo.serialize()

                return diet_info, 200

            return 'Plan not selected', 404

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


# Exercise


class GetExercisePlan(Resource):

    def get(self):

        try:
            plans_db = Exerciseplan.query.all()

            plans = []
            for plan in plans_db:

                plans.append(plan.serialize())

            return plans,  200

        except:
            return 'Server error', 401


class ExercisePlan(Resource):

    method_decorators = [admin_required]

    def post(self):

        try:
            new_plan = request.get_json()

            checkPlan = Exerciseplan.query.filter(
                Exerciseplan.name == new_plan['name']).first()

            if checkPlan:

                return 'Exercise already exist', 401

            plan_name = new_plan['name']
            plan_pic = new_plan['pic']
            beginner = json.dumps(new_plan['beginner'])
            intermidate = json.dumps(new_plan['intermidate'])
            advanced = json.dumps(new_plan['advanced'])

            new_plan = Exerciseplan(
                plan_name, plan_pic, beginner, intermidate, advanced)

            db.session.add(new_plan)
            db.session.commit()

            return 'success', 200

        except:
            return 'Server error', 401

    def put(self):

        try:
            update_plan_body = request.get_json()

            checkPlan = Exerciseplan.query.filter(
                Exerciseplan.name == update_plan_body['name']).first()

            if checkPlan:

                checkPlan.name = update_plan_body['name']
                checkPlan.pic = update_plan_body['pic']
                checkPlan.beginner = json.dumps(update_plan_body['beginner'])
                checkPlan.intermidate = json.dumps(
                    update_plan_body['intermidate'])
                checkPlan.advanced = json.dumps(update_plan_body['advanced'])

                db.session.add(checkPlan)
                db.session.commit()

                return 'success', 200

            return 'No exercise found', 404

        except:
            return 'Server error', 401

    def delete(self):

        try:
            deleted_plan_name = request.headers['name']

            checkPlan = Exerciseplan.query.filter(
                Exerciseplan.name == deleted_plan_name).first()

            if checkPlan:

                db.session.delete(checkPlan)
                db.session.commit()

                return 'success', 200

            return 'No exercise found', 404

        except:
            return 'Server error', 401


# Diet
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

    def delete(self):

        try:
            deleted_diet_name = request.headers['name']

            checkDiet = Diet.query.filter(
                Diet.name == deleted_diet_name).first()

            if checkDiet:

                db.session.delete(checkDiet)
                db.session.commit()

                return 'success', 200

            return 'No diet found', 404

        except:
            return 'Server error', 401

# Timeline


class TodaysTimeline(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        try:
            user_id = current_user.user_id
            currentDay = dt.now().day
            currentMonth = dt.now().month
            currentYear = dt.now().year

            current_date = currentDay + '/' + currentMonth + '/' + currentYear

            todays_timeline = Timeline.query.filter(
                Timeline.user_id == user_id, Timeline.date == current_date).first()

            if todays_timeline:

                if todays_timeline.status == 'done':
                    return 'Already done', 401

                return todays_timeline.serialize(), 200

            plan_id = getPlanId(user_id)
            level = getLevel(user_id)

            today_workouts = getTodaysWorkouts(plan_id, level)
            todays_timeline = Timeline(
                current_date, user_id, plan_id, today_workouts, 'not')

            return todays_timeline, 200

        except:
            return 'Server error', 401


class UserTimeline(Resource):

    method_decorators = [token_required]

    def get(self, current_user):

        try:
            timeline_db = Timeline.query.filter(
                Timeline.user_id == current_user.user_id).all()

            timelines = []
            for timeline in timeline_db:

                timelines.append(timeline.serialize())

            return timelines,  200

        except:
            return 'Server error', 401

    def put(self, current_user):

        try:
            update_timeline_body = request.get_json()
            user_id = current_user.user_id
            date = update_timeline_body['date']

            checkTimeline = Timeline.query.filter(
                Timeline.user_id == user_id, Timeline.date == date).first()

            if checkTimeline:

                checkTimeline.status = 'done'
                checkTimeline.exercises = json.dumps(
                    update_timeline_body['workouts'])

                db.session.add(checkTimeline)
                db.session.commit()

                return 'success', 200

            return 'No timeline found', 404

        except:
            return 'Server error', 401

    def delete(self, current_user):

        try:
            resetTimeline(current_user.id)
            return 'success', 200

        except:
            return 'Server error', 401


# Endpoints
# User
api.add_resource(CheckUserAuthenticity, '/api/isUser/')
api.add_resource(Login, '/api/login/')
api.add_resource(Signup, '/api/signup/')
api.add_resource(ResetPassword, '/api/forgetPassword/')
api.add_resource(UpdatePassword, '/api/updatePassword/')
api.add_resource(User, '/api/user/')
api.add_resource(UserStatus, '/api/userStatus/')
api.add_resource(UserExercisePlan, '/api/userExercisePlan/')
api.add_resource(UserDietPlan, '/api/userDietPlan/')

# Admin
api.add_resource(RevokeUser, '/api/revokeUser/')
api.add_resource(AllowUser, '/api/allowUser/')
api.add_resource(AddAdmin, '/api/newAdmin/')
api.add_resource(GeneralReport, '/api/report')

# Exercise
api.add_resource(ExercisePlan, '/api/exercisePlan/')
api.add_resource(GetExercisePlan, '/api/allExercisePlans/')

# Diet
api.add_resource(DietPlan, '/api/diet/')

# Timeline
api.add_resource(TodaysTimeline, '/api/todayTimeline')
api.add_resource(UserTimeline, '/api/userTimeline')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
