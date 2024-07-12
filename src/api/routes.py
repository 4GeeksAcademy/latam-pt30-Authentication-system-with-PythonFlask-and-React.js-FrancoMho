"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#### SIGN UP
#[POST] /users Create users. 
@api.route("/user", methods=["POST"])
def create_user():
    #Extract data from request
    data = request.json
    #Verifying we are receiving all required data in the request
    email = data.get("email")
    password  = data.get("password")

    #Returning 400 if data is not correct  
    if not email or not password:
        return jsonify({
            "message": "Email and Password are Required"
        }), 400
    #Email Verification
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Invalid email"}), 400
    
    #We create new user
    new_user = User(email=email, password=password, is_active=True)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({"message": "User created successfully"}), 201


##LOGIN
# token
@api.route("/token", methods=["POST"])
def login_user():
   #Extract data from request
    data = request.json
    #Verifying we are receiving all required data in the request
    email = data.get("email")
    password = data.get("password")

    #Returning 400 if data is not correct  
    if not email or not password:
        return jsonify({
            "message": "Email and Password are Required"
        }), 400

    user = User.query.filter_by(email=email).first()
    print(user)

    if user is None:
        return jsonify({
            "message": "Email or password invalid"
        }), 400
    

    password_is_valid = data["password"]
    
    if not password_is_valid:
        return jsonify({
            "message": "Email or password invalid"
        }), 400
    
    token = create_access_token(identity=user.id)
    response_body={
        "token": token,
        "user": user.serialize()
    }
    return jsonify(response_body), 201


####LOGIN WITH A JWT REQUIRED -- USERS can see other users info
#[GET] /user/int:id> Get user
# @api.route("/user/<int:id>", methods=['GET'])
# #@jwt_required()
# def get_user_data(id):
#     user = User.query.get(id)
#     if not user:
#         return jsonify({"message": "User not found"}), 400
#     return jsonify(
#         {
#             "user": {
#                 "email": user.email,
#                 "password": user.password,
#                 #"ig_password": user.ig_password,
#                 "is_active": user.is_active
#             }
#         }
#     ), 200


##PERSONALPRIVATE VIEW --- USERS only can see theirs info
#[GET] /user/id Get user ig
@api.route("/user/id", methods=['GET'])
@jwt_required()
def get_user_ig():
    user_id= get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 400
    return jsonify(
        {
            "user": {
                "email": user.email,
                "password": user.password,
                #"private_info": user.private_info,
                "is_active": user.is_active
            }
        }
    ), 200