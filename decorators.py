from flask import request
from model import *
from functools import wraps
import jwt
from settings import SECERET_KEY


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return "Token is required!", 401

        try:
            data = jwt.decode(token, SECERET_KEY, algorithms=["HS256"])
            current_user = Users.query.filter(
                Users.email == data['email']).first()
            is_user_allowed = LoginInfo.query.filter(
                LoginInfo.email == current_user.email).first()
            if is_user_allowed == None:
                return "Account is blocked!", 400
        except:

            return "Token is invalid!", 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return "Token is invalid!", 401

        try:

            data = jwt.decode(token, SECERET_KEY, algorithms=["HS256"])
            current_user = Admin.query.filter(
                Admin.email == data['email']).first()
            is_admin_allowed = LoginInfo.query.filter(
                LoginInfo.email == current_user.email).first()
            if is_admin_allowed == None:
                return "Account is blocked!", 400
        except:

            return "Token is invalid!", 401

        return f(current_user, *args, **kwargs)

    return decorated
