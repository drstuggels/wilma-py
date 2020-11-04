from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from wilma import fetch
import json

app = Flask(__name__)
CORS(app)
api = Api(app)


class Next_Lesson(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        try:
            schedule = fetch(args["url"], args["username"], args["password"])
        except:
            return {"message": "Fail"}, 500
        next_lesson = schedule.next_lesson()
        if next_lesson == False or next_lesson == []:
            return {"message": "Success", "next": []}, 200
        else:
            return {"message": "Success", "next": next_lesson.to_dict()}, 200


api.add_resource(
    Next_Lesson, '/next')
