from model import *
import datetime
import re


def checkLen(item, lenght):

    try:
        if len(item) < lenght:

            return False

        return True

    except:
        return False


def isBetween(value, start, end):

    try:
        if value >= start and value <= end:

            return True

        return False

    except:
        return False


def valEmail(email):

    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if(re.fullmatch(regex, email)):

            return True

        return False

    except:
        return False


def isUsernameUnique(username):

    try:
        isUsername = Users.query.filter(Users.username == username).first()

        if isUsername:

            return False

        return True

    except:
        return False


def isEmailUnique(email):

    try:
        isEmail = Users.query.filter(Users.email == email).first()

        if isEmail:

            return False

        return True

    except:
        return False


def calBMI(height, weight):

    try:
        bmi = weight / (height * height)
        return bmi

    except:
        return 0.0


def calFat(age, bmi):

    try:
        fat_percentage = (1.20 * bmi) + (0.23 * age) - 16.2
        return fat_percentage

    except:
        return 0.0


def calCalorieIntake(age):

    try:
        if age == 2 | age == 3:

            return 1000

        elif age in range(9, 13):

            return 1600

        elif age in range(14, 18):

            return 1800

        elif age in range(19, 30):

            return 2000

        elif age in range(31, 50):

            return 1200

        else:

            return 1600

    except:
        return 0.0


def getLevel(user_id):

    try:
        userPlanInfo = UserPlan.query.filter(
            UserPlan.user_id == user_id).first()

        if userPlanInfo:

            level = userPlanInfo.level

            return level

        return False

    except:

        return False


def updateLevel(user_id, plan_id, level):

    try:
        PlanInfo = Exerciseplan.query.filter(
            Exerciseplan.plan_id == plan_id).first()

        levels = ['beginner', 'intermidate', 'advanced']
        level = levels.index(level)

        if PlanInfo:

            levels_info = [json.loads(PlanInfo.beginner), json.loads(
                PlanInfo.intermidate), json.loads(PlanInfo.advanced)]

            current_level = levels_info[level]
            goal = current_level['goal']

            workout_histroy = Timeline.query.filter(
                Timeline.user_id == user_id, Timeline.level == current_level, Timeline.status == 'Done').all()

            weeks_done = int(len(workout_histroy) / 7)

            if weeks_done >= int(goal):

                next_level = level

                if level < 2:

                    next_level += 1

                userPlanInfo = UserPlan.query.filter(
                    UserPlan.user_id == user_id).first()

                if userPlanInfo:

                    userPlanInfo.level = levels[next_level]
                    db.session.add(userPlanInfo)
                    db.session.commit()

    except:

        return False


def getWorkouts(plan_id, level):

    try:
        PlanInfo = Exerciseplan.query.filter(
            Exerciseplan.plan_id == plan_id).first()

        levels = ['beginner', 'intermidate', 'advanced']
        level = levels.index(level)

        if PlanInfo:

            plan_info = PlanInfo.serialize()
            workouts = plan_info[levels[level]]

            return workouts

    except:

        return False

def getTodaysWorkouts(plan_id, level):

    try:
        PlanInfo = Exerciseplan.query.filter(
            Exerciseplan.plan_id == plan_id).first()

        levels = ['beginner', 'intermidate', 'advanced']
        level = levels.index(level)
        today = datetime.datetime.now().strftime("%A").lower()

        if PlanInfo:

            plan_info = PlanInfo.serialize()
            workouts = plan_info[levels[level][today]]

            return workouts

    except:

        return False


def resetTimeline(user_id):

    try:
        userTimeline = Timeline.query.filter(
            Timeline.user_id == user_id).all()

        if userTimeline:

            for timeline in userTimeline:

                db.session.delete(timeline)
                db.session.commit()

    except:

        return False


def delPlan(user_id):

    try:
        userPlan = UserPlan.query.filter(
            UserPlan.user_id == user_id).first()

        if userPlan:

            db.session.delete(userPlan)
            db.session.commit()

    except:

        return False


def getPlanName(plan_id):

    try:
        PlanInfo = Exerciseplan.query.filter(
            Exerciseplan.plan_id == plan_id).first()

        if PlanInfo:

            plan_name = PlanInfo.name

            return plan_name

        return False

    except:
        return False


def getPlanId(user_id):

    try:
        userPlanInfo = UserPlan.query.filter(
            UserPlan.user_id == user_id).first()

        plan_id = userPlanInfo.plan_id

        return plan_id

    except:
        return False

def getWeek(user_id):

    try:
        userPlanInfo = UserPlan.query.filter(
            UserPlan.user_id == user_id).first()

        week = userPlanInfo.week

        return week

    except:
        return False


def getPlanGoal(user_id):

    try:
        level = getLevel(user_id)
        plan_id = getPlanId(user_id)

        PlanInfo = Exerciseplan.query.filter(
            Exerciseplan.plan_id == plan_id).first()

        if PlanInfo:

            levels = ['beginner', 'intermidate', 'advanced']
            level = levels.index(level)

            plan_info = PlanInfo.serialize()
            goal = plan_info[levels[level]['goal']]

            return goal

    except:
        return False


def updateWeek(user_id):

    try:

        workout_histroy = Timeline.query.filter(
            Timeline.user_id == user_id).all()

        weeks_done = int(len(workout_histroy) / 7)

        userPlanInfo = UserPlan.query.filter(
            UserPlan.user_id == user_id).first()

        userPlanInfo.week = weeks_done
        db.session.add(userPlanInfo)
        db.session.commit()

    except:

        return False
