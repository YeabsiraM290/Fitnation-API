from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from settings import *
from model import *

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
 api.add_resource(User, '/api/User/')

if __name__ == "__main__":
    app.run(debug=True) 
