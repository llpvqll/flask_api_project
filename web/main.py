# registration of a user
# each user gets 10 tokens
# store a sentence on our database for 1 token
# retrieve his stored sentence on out database for 1 token

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["users"]


class Register(Resource):
    def post(self):
        # get posted data by the user
        posted_data = request.get_json()

        # get the data

        username = posted_data['username']
        password = posted_data["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store username and pw into the database

        users.insert_one({
            'username': username,
            'password': hashed_pw,
            'sentence': '',
            'tokens': 6
        })

        ret_json = {
            'status': 200,
            'message': 'You successfully signed up for the API'
        }
        return jsonify(ret_json)


def verify_pw(username, password):
    hashed_pw = users.find({
        "username": username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
        "username": username
    })[0]["tokens"]

    return tokens


class Store(Resource):
    def post(self):
        # get the posted data
        posted_data = request.get_json()

        # read the data
        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']

        # verify the username ps match
        correct_pw = verify_pw(username, password)

        if not correct_pw:
            ret_json = {
                'status': 302
            }
            return jsonify(ret_json)
        # verify user has enough tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            ret_json = {
                'status': 301
            }
            return jsonify(ret_json)
        # store the sentence and return 200 OK
        users.update_one({
            "Username": username,

        }, {
            "$set": {
                "Sentence": sentence,
                "Tokens": num_tokens-1
            }
        })
        ret_json = {
            'status': 200,
            'message': "Sentence saved successfully"
        }
        return jsonify(ret_json)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


# from flask import Flask, jsonify, request
# from flask_restful import Api, Resource
# import os
# from pymongo import MongoClient
#
# app = Flask(__name__)
# api = Api(app)
#
# client = MongoClient("mongodb://db:27017")
# db = client.aNewDB
# UserNum = db["UserNum"]
#
# UserNum.insert_one({
#     'num_of_users': 0
# })
#
#
# class Visit(Resource):
#     @staticmethod
#     def get():
#         prev_num = UserNum.find({})[0]['num_of_users']
#         new_num = prev_num + 1
#         UserNum.update_one({}, {"$set": {"num_of_users": new_num}})
#         return str("Hello user " + str(new_num))
#
#
# def check_posted_data(posted_data, function_name):
#
#     if function_name == 'add' or function_name == 'subtract' \
#             or function_name == 'multiply' or function_name == 'divide':
#         if "x" not in posted_data or "y" not in posted_data:
#             return 301
#         elif int(posted_data['y']) == 0:
#             return 302
#         else:
#             return 200
#
#
# class Add(Resource):
#     @staticmethod
#     def post():
#         # If I am here, then the resource Add was requested using the method POST
#         # Get posted data:
#         posted_data = request.get_json()
#
#         # Verify validity of posted data
#         status_code = check_posted_data(posted_data, 'add')
#         if status_code != 200:
#             ret_json = {
#                 'Message': 'An error happened',
#                 'Status code': status_code
#             }
#             return jsonify(ret_json)
#
#         # If I am here, the status_code == 200
#         x = posted_data['x']
#         y = posted_data['y']
#         x = int(x)
#         y = int(y)
#
#         # Add the posted data:
#         ret = x + y
#         ret_map = {
#             'Message': ret,
#             'Status code': status_code
#         }
#         return jsonify(ret_map)
#
#
# class Subtract(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         status_code = check_posted_data(posted_data, 'subtract')
#
#         if status_code != 200:
#             ret_json = {
#                 'Message': 'An error happened',
#                 'Status code': status_code
#             }
#             return jsonify(ret_json)
#
#         x = posted_data['x']
#         y = posted_data['y']
#         x = int(x)
#         y = int(y)
#
#         ret = x - y
#         ret_map = {
#             'Message': ret,
#             'Status code': status_code
#         }
#         return jsonify(ret_map)
#
#
# class Multiply(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         status_code = check_posted_data(posted_data, 'multiply')
#
#         if status_code != 200:
#             ret_json = {
#                 'Message': 'An error happened',
#                 'Status code': status_code
#             }
#             return jsonify(ret_json)
#
#         x = posted_data['x']
#         y = posted_data['y']
#         x = int(x)
#         y = int(y)
#
#         ret = x * y
#         ret_map = {
#             'Message': ret,
#             'Status code': status_code
#         }
#         return jsonify(ret_map)
#
#
# class Divide(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         status_code = check_posted_data(posted_data, 'divide')
#
#         if status_code != 200:
#             ret_json = {
#                 'Message': 'An error happened',
#                 'Status code': status_code
#             }
#             return jsonify(ret_json)
#
#         x = posted_data['x']
#         y = posted_data['y']
#         x = int(x)
#         y = int(y)
#
#         ret = x / y
#         ret_map = {
#             'Message': ret,
#             'Status code': status_code
#         }
#         return jsonify(ret_map)
#
#
# api.add_resource(Add, '/add')
# api.add_resource(Subtract, '/subtract')
# api.add_resource(Multiply, '/multiply')
# api.add_resource(Divide, '/division')
# api.add_resource(Visit, '/hello')
#
#
# @app.route('/')
# def hello_world():
#     return "Hello World"
#
#
# if __name__ == "__main__":
#
#     app.run(host='0.0.0.0', debug=True)
