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
    email_in_data = data.get("email")
    password_in_data = data.get("password")
    #Returning 400 if data is not correct  
    if None in [email_in_data, password_in_data]:
        return jsonify({
            "message": "Email and Password are Required"
        }), 400
    #Email Verification
    user_email = email_in_data
    user_password = password_in_data
    user_already_exists = db.session.execute(db.select(User).filter_by(email= user_email)).one_or_none()
    
    if user_already_exists:
        return jsonify({"message": "Invalid email"}), 400
    
    #We create new user
    new_user = User(email=user_email, password=user_password, is_active=True)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()
        return jsonify({"message":"Error in server"}), 500
    return jsonify({}), 201


##LOGIN
# token
@api.route("/token", methods=["POST"])
def login_user():
   #Extract data from request
    data = request.json
    #Verifying we are receiving all required data in the request
    email_in_data = data.get("email")
    password_in_data = data.get("password")
    #Returning 400 if data is not correct  
    if None in [email_in_data, password_in_data]:
        return jsonify({
            "message": "Email and Password are Required"
        }), 400

    user = User.query.filter_by(email=data["email"]).first()
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
    
    token = create_access_token(identity=email_in_data)
    response_body={
        "token": token,
        "user": user.serialize()
    }
    return jsonify(response_body), 201


####LOGIN WITH A JWT REQUIRED -- USERS can see other users info
#[GET] /user/int:id> Get user
@api.route("/user/<int:id>", methods=['GET'])
#@jwt_required()
def get_user_data(id):
    user_result = db.session.execute(db.select(User).filter_by(id=id)).one_or_none()
    user =user_result[0]
    return jsonify(
        {
            "user": {
                "email": user.email,
                "password": user.password,
                #"ig_password": user.ig_password,
                "is_active": user.is_active
            }
        }
    ), 200


##PERSONALPRIVATE VIEW --- USERS only can see theirs info
#[GET] /user/ig Get user ig
@api.route("/user/ig", methods=['GET'])
@jwt_required()
def get_user_ig():
    user_id= get_jwt_identity()
    user_result = db.session.execute(db.select(User).filter_by(id= user_id))
    user =user_result[0]
    return jsonify(
        {
            "user": {
                "email": user.email,
                "password": user.password,
                "ig_password": user.ig_password,
                "is_active": user.is_active
            }
        }
    ), 200