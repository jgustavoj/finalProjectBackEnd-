"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
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

notification = Notifications()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/process_notifications', methods=['GET'])
# def process_notifications():
#     events_query = Event.query.all()
#     all_events = list(map(lambda x: x.serialize(), events_query))
#     today_date = datetime.datetime.now()
#     year_date = today_date[0:4]
#     month_date = today_date[5:7]
#     day_date = today_date[8:10]

#     x = datetime.datetime(year, month, day)
#     y = datetime.datetime(start_year, start_month, start_day)
#     z = y - x

#         for event in all_events: 
#             if z == 1:
# 	            send(body="Your event is one day away")
#             if z == 7:
# 	            send(body="Your event is one week away")
    
#         return jsonify(), 200   

# @app.route('/events', methods=['POST'])
# def post_item():
#     request_body = json.loads(request.data)
#     event = Event(startDate=request_body["startDate"], title=request_body["title"])
#     db.session.add(event)
#     db.session.commit()
#     event_query = Event.query.all()
#     all_event = list(map(lambda x: x.serialize(), event_query))
#     return jsonify(all_event), 200


# @app.route('/events/<int:id>', methods=['DELETE'])
# def delete_item(id):
#     event = Event.query.get(id)
#     if event is None:
#         raise APIException('event not found', status_code=404)
#     db.session.delete(event)
#     db.session.commit()
#     event_query = Event.query.all()
#     all_event = list(map(lambda x: x.serialize(), event_query))
#     return jsonify(all_event), 200
@app.route('/appointments/<int:id>', methods=['PUT', 'GET'])
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
        return jsonify(appointment.serialize()), 200

    return "Invalid Method", 404

@app.route('/appointments', methods=['POST', 'GET'])
def handle_appointment():
    """
    Create an appoitnment
    """
    # POST request
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
       
        appointment = Appointment(title=body['title'], startDate=body['startDate'], endDate=body['endDate'], location=body['location'])
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
def delete_item(id):
    appointment = Appointment.query.get(id)
    if appointment is None:
        raise APIException('Appointment not found', status_code=404)
    db.session.delete(appointment)
    db.session.commit()
    appointment = Appointment.query.all()
    appointment = list(map(lambda x: x.serialize(), appointment))
    return jsonify(appointment), 200



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

