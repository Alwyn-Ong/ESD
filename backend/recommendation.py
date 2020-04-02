#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS
import time

# For AMQP
import pika
import uuid

# For HTTP Calls
import requests

# Obtains function from profile
import profile

# Stores url of microservices for HTTP Call
profileURL = "http://localhost:2000"

app = Flask(__name__)
# Database name in this case is match
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_recommendation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)


# Creates a recommendation class to interact with the database
class Recommendation(db.Model):
    __tablename__ = 'recommendation'

    visit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    visited_id = db.Column(db.Integer)
    like_status = db.Column(db.Boolean)

    def __init__(self, user_id, visited_id, like_status, visit_id = None):
        self.visit_id = visit_id
        self.user_id = user_id
        self.visited_id = visited_id
        self.like_status = like_status

    # return an order item as a JSON object
    def json(self):
        return {'visit_id': self.visit_id, 'user_id': self.user_id, 'visited_id': self.visited_id}

def send_match_update(user_id,visited_id):
    """
    Sends message (as a json_string) to match_receiver.py, containing the following:

    {
        "userid":user_id,
        "visitedid":visited_id
    }

    Function will trigger when the user ends up liking a person that likes you back.

    Allows recommendation to send a one-to-one fire-and-forget message to match_receiver.py

    Match_receiver.py will update the new match using the 2 ids using a function call to match.

    
    """
    # default username / password to the broker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="recommendation_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    json_message = {"userid":user_id,"visitedid":visited_id}

    message = json.dumps(json_message, default=str) # convert a JSON object to a string

    # prepares the corrid
    corrid = str(uuid.uuid4())

    # request from profile and exit, leaving it to order_reply to handle replies
        # Prepare the correlation id and reply_to queue and do some record keeping
    # replyqueuename = "profile.reply"
    # prepare the channel and send a message to Shipping
    channel.queue_declare(queue='match', durable=True) # make sure the queue used by profile exist and durable
    channel.queue_bind(exchange=exchangename, queue='match', routing_key='match.create') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="match.create", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            # reply_to=replyqueuename, # set the reply queue which will be used as the routing key for reply messages
            correlation_id = corrid # Sets the userid as corrid
        )
    )
    # print("Order sent to shipping.")
    # close the connection to the broker
    connection.close()

@app.route("/recommendation/<int:userid>",methods=["GET"])
def get_recommendation(userid):
    """
    Retrieves a recommendation, based on user.

    Takes in an url in the format

    /recommendation/1 where 1 would be the userid

    Returns the details of the first recommended person's 
    ID (by cross checking profiles with visited)
    profile (by accessing profile microservice) 
    """
    # Gets the variables from the url
  
    # Gets a list of profiles through HTTP Call
    # Uses get_all function (/allprofiles)
    profile_request_url = profileURL + "/allprofiles"
    
    r = requests.get(profile_request_url) # the reply 'r' is no use

    # Obtains a dictionary from json reply
    result = r.json()

    profiles = result["all profiles"]


    # First finds the gender of the user by getting from the user profile
    
    for profile in profiles:
        if profile["profileid"] == userid:
            gender = profile["gender"]

    # Stores a list of profiles (excluding original userid)
    profile_list = []

    # Next generates a list of relevant profiles to choose from
    for profile in profiles:

        # Adds if not the user and different gender
        if profile["profileid"] != userid and profile["gender"] != gender:
            profile_list.append(profile)

    # Finds an appropiate person to return
    for profile in profile_list:
        profile_id = profile["profileid"]

        # Currently prioritises people that already like you

        # First checks for people that already like user
        if (Recommendation.query.filter_by(user_id=int(profile_id),visited_id=int(userid),like_status="1").first() != None
            
            # Next checks if you have already visited the person
            and Recommendation.query.filter_by(user_id=int(userid),visited_id=int(profile_id)).first() == None):

            # return json.dumps(str(type(profile["profileid"])))
            # return json.dumps(str(type(userid)))
            return jsonify(profile)

    for profile in profile_list:
        profile_id = profile["profileid"]

        # Else return a user that you have already visited
        if Recommendation.query.filter_by(user_id=int(userid),visited_id=int(profile_id)).first() == None:
            return jsonify(profile)


@app.route("/recommendation/",methods=["POST"])
def store_visited():
    """
    Stores the visitation of id1 visiting id2

    Takes in json data in the format
    {
        "id1":"1",
        "id2":"2",
        "like_status":"0/1" - 0 for false, 1 for true
    }

    First checks if the opposing user has liked the user

    if yes, creates a subsequent row in match for storage

    If there is an error creating row in recommendation DB, return error message. 

    Returns in the format

    {
        "status":"" -> success/failure (if there is no match, in adding to recommendation DB
                        /match (if there is a match)
        "userid":1 -> userid of opposiing user matched
    }

    """

    data = request.get_json()

    # Currently the data is in string format

    user_id = int(data["id1"])
    visited_id = int(data["id2"])
    like_status = int(data["like_status"])

    # Checks if there are currently any existing matches in the database

    visited_check = Recommendation.query.filter_by(user_id=user_id, visited_id=visited_id).first()

    if visited_check != None:
        return jsonify({"status":"failure","message": f"The record where {user_id} has visited {visited_id} already exists."}), 500

    # Creates a record in recommendation regardless

    recommendation = Recommendation(user_id,visited_id,like_status)

    try:
        db.session.add(recommendation)
        db.session.commit()
    except Exception as e:
        return jsonify({"status":"failure","message": f"An error {e} occured creating the match.","userid":visited_id}), 500

    # If the user clicked like, checks if the opposing user likes the user as well
    if like_status == 1 and Recommendation.query.filter_by(user_id=visited_id,visited_id=user_id,like_status = 1).first() != None:
        
        # Sends a message to match receiver to create a new record in match
        send_match_update(user_id,visited_id)

        # Create subsequent row in chat DB, using HTTP Call to chat ms
        

        # Returns Match status along with userid
        return jsonify({"status":"match","message":"You have a match!","userid":user_id})

    # Returns Success status along with userid
    return jsonify({"status":"success","message":"Successfully added into the database","userid":visited_id})


if __name__ == "__main__":
    app.run(port=9000,debug=True)
