"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Appointment
from sms import send
import datetime
from datastructures import Notifications 


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


"""
JWT Login Route Thread 

"""

#login was commented for frontend login testing 

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    # this line filters the Users db and checks if email = "dynamic" email, meaning - did the user register the email into the db 
    user_check = User.query.filter_by(email=email, password=password).first()
    # print("$$$ ", user_check)
    if user_check==None:  
        return jsonify({"msg": "Incorrect email or password, please try again"}), 401
    
    # Identity can be any data that is json serializable
    # user = {    
    #     'access_token': create_access_token(identity=user_check.id),
    #     'user_info':  user_check.serialize()
    # }
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=user_check.id, expires_delta=expires) 

    # return jsonify(user), 200
    return jsonify(access_token), 200

"""
User Routes Thread

"""

@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create Single User

    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        user = User(first_name=body['first_name'], last_name=body["last_name"], email=body['email'], phone_number=body["phone_number"], password=body['password']) 
        db.session.add(user)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        user = User.query.all()
        user = list(map(lambda x: x.serialize(), user))
        return jsonify(user), 200
    return "Invalid Method", 404


@app.route('/user/<int:id>', methods=['PUT', 'GET'])
def get_single_user(id):
    """
    Update Single user

    """
    body = request.get_json() #{ 'email': 'new_email'}
    # PUT Method
    if request.method == 'PUT':
        user = User.query.get(id)
        user.email = body["email"]
        user.password = body["password"]
        user.first_name = body["first_name"]
        user.last_name = body["last_name"]
        user.phone_number = body["phone_number"]
        db.session.commit()
        return jsonify(user.serialize()), 200
    # GET Method
    if request.method == 'GET':
        user = User.query.get(id)
        user = list(map(lambda x: x.serialize(), user))
        return jsonify(user), 200
    return "Invalid Method", 404

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete Single User
    
    """

    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    user = User.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user), 200


""" 
Appointment Routes Thread

"""


@app.route('/appointments/<int:id>', methods=['PUT', 'GET'])
@jwt_required
def handle_appointment_update(id):
    """
    Update Appointment
    """
    body = request.get_json() 
    if request.method == 'PUT':
        appointment = Appointment.query.get(id)
        appointment.title = body["title"]
        appointment.location = body["location"]
        appointment.startDate = body["startDate"]
        appointment.endDate = body["endDate"]
        db.session.commit()
        return jsonify(appointment.serialize()), 200
    if request.method == 'GET':
        appointment = Appointment.query.get(id)
        appointment = list(map(lambda x: x.serialize(), appointment))
        return jsonify(appointment), 200
        #return jsonify(appointment.serialize()), 200
    return "Invalid Method", 404



@app.route('/appointments', methods=['POST', 'GET'])
@jwt_required # this requires a valid access toke in the request to access. Look at line appointment = Appointment(title etc..)
def handle_appointment():
    """
    Create an appoitnment with user relationship 
    """
    user_id= get_jwt_identity() # from jwt to recognize the user - belongs to specific user. This line is ONLY used if were creating relationship between 2 databases. 
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        appointment = Appointment(title=body['title'], startDate=body['startDate'], endDate=body['endDate'], location=body['location'],  user_id=user_id) # user_id=user_id is from db (user id from user) 
        db.session.add(appointment)
        db.session.commit()
        return "ok", 200
    # GET request
    if request.method == 'GET':
        appointment = Appointment.query.all()
        appointment = list(map(lambda x: x.serialize(), appointment))
        return jsonify(appointment), 200
    return "Invalid Method", 404

# DELETE request no Twilio 
@app.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required
def delete_item(id):
    appointment = Appointment.query.get(id)
    if appointment is None:
        raise APIException('Appointment not found', status_code=404)
    db.session.delete(appointment)
    db.session.commit()
    appointment = Appointment.query.all()
    appointment = list(map(lambda x: x.serialize(), appointment))
    return jsonify(appointment), 200


"""

Twillio Routes Thread

"""
# notification = Notifications()

#this delete method is only used for TWILIO 
# @app.route('/notification', methods=['DELETE'])
# def dequeue():
#     event = notification.dequeue()
#     event_name = event['title']
#     event_date = event['startDate']
#     send(body="Your " + event_name + " is coming up on " + event_date)
#     return jsonify("Texted"), 200    





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
