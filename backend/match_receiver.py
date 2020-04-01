from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import sys

# Obtains function from profile
import match

# For messaging/AMQP

import pika
import uuid

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_profile'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# db = SQLAlchemy(app)
# CORS(app)

# class profile(db.Model):
#     __tablename__ = 'profiledetails'

#     profileID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
#     name = db.Column(db.VARCHAR(50), nullable=False)
#     bio = db.Column(db.String(2083), nullable=False)
#     gender = db.Column(db.String(1), nullable=False)
#     age = db.Column(db.Integer(), nullable=False)
#     location = db.Column(db.VARCHAR(255), nullable=False)

#     def __init__(self, profileID, name, bio, gender, age, location):
#         self.profileID = profileID
#         self.name = name
#         self.bio = bio
#         self.gender = gender
#         self.age = age
#         self.location = location

#     def json(self):
#         return {"profileid": self.profileID, "bio": self.bio, "gender": self.gender, "age": self.age, "location":self.location}

def receiveOrder():
    hostname = "localhost" # default hostname
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="recommendation_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')
    
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="match", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='match.create') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received a match from recommendation")
    
    with match.app.test_request_context('/match/'):
        # print("The body is")
        # print(type(body))
        # print(body)
        # print(body.decode("UTF-8"))
        print(f"Message received: {json.loads(body)}")
        data = json.loads(body)
        id1 = data["userid"]
        # print(id1)
        id2 = data["visitedid"]
        # print(id2)
        result = match.add_match(id1,id2)

    # print("Type is ")
    # print(type(result))
    # print(result)
    print(f"Message from match {result[0].get_json()}")
    # result = json.dumps(result,default=str)
    # result = get_all()
    # result = processOrder(json.loads(body))
    # json.dump(result, sys.stdout, default=str)
    # print processing result; not really needed
    # json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    # print() # print another new line as a separator

    # prepare the reply message and send it out
    # replymessage = json.dumps(result, default=str) # convert the JSON object to a string
    # replyqueuename="profile.reply"

    # A general note about AMQP queues: If a queue or an exchange doesn't exist before a message is sent,
    # - the broker by default silently drops the message;
    # - So, if really need a 'durable' message that can survive broker restarts, need to
    #  + declare the exchange before sending a message, and
    #  + declare the 'durable' queue and bind it to the exchange before sending a message, and
    #  + send the message with a persistent mode (delivery_mode=2).
    
    # set up the exchange if the exchange doesn't exist
    # exchangename="recommendation_direct"
    # channel.exchange_declare(exchange=exchangename, exchange_type='direct')
        
    # channel.queue_declare(queue=replyqueuename, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    # channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key=replyqueuename) # make sure the reply_to queue is bound to the exchange
    # channel.basic_publish(exchange=exchangename,
    #         routing_key=properties.reply_to, # use the reply queue set in the request message as the routing key for reply messages
    #         body=result, 
    #         properties=pika.BasicProperties(delivery_mode = 2, # make message persistent (stored to disk, not just memory) within the matching queues; default is 1 (only store in memory)
    #             correlation_id = properties.correlation_id, # use the correlation id set in the request message
    #         )
    # )
    channel.basic_ack(delivery_tag=method.delivery_tag) # acknowledge to the broker that the processing of the request message is completed

# def processOrder(order):
#     print("Processing an order:")
#     print(f"order is {order}")
#     # Can do anything here. E.g., publish a message to the error handler when processing fails.
#     # resultstatus = bool(random.getrandbits(1)) # simulate success/failure with a random True or False
#     # result = {'status': resultstatus, 'message': 'Simulated random shipping result.', 'order': order}
#     # return get_all

#     result = get_all()
#     # print(result)
#     if result != None:
#         return result
#     return jsonify({"message":"There was an error retrieving from the database."})
#     # resultmessage = json.dumps(result, default=str) # convert the JSON object to a string
#     # if not resultstatus: # inform the error handler when shipping fails
#     #     print("Failed shipping.")
#     #     send_error(resultmessage)
#     # else:
#     #     print("OK shipping.")
#     # return result

# ## retrieve all profiles
# @app.route("/allprofiles")
# def get_all():
#     #check if its only called by matching service then can call this service
#     return jsonify({"all profiles": [profiles.json() for profiles in profile.query.all()]})    

# #retrieve current profile (used as placeholder to edit)
# @app.route("/profile/<int:profileid>")
# def find_by_userid(profileid):
#     userprofile = profile.query.filter_by(profileID=profileid).first()
#     if userprofile:
#         return jsonify(userprofile.json())
#     return jsonify({"message": "profile not found"}), 404

# #update profile
# @app.route("/updateprofile",methods=['PUT'])
# def update_profile():
#     #profileID hardcoded for now
#     profileID = 1
#     ##
#     userprofile = profile.query.filter_by(profileID=profileID).first()
#     #update the entire profile
#     data = request.get_json()
#     location = data['location']
#     userprofile.location = location
#     bio = data['bio']
#     userprofile.bio = bio
#     gender = data['gender']
#     userprofile.gender = gender
#     age = data['age']
#     userprofile.age = age
#     name = data['name']
#     userprofile.name = name

#     try:
#         db.session.commit()
#     except:
#         return jsonify({"message": "An error occurred in updating the book."}), 500

#     return "201"

# #create profile 
# @app.route("/profile", methods=['POST'])
# def create_profile():
#     ##profileID not suposed to be given
#     profileID = request.json['profileID']
#     ##hardcoded for now
#     name = request.json['name']
#     location = request.json['location']
#     bio = request.json['bio']
#     gender = request.json['gender']
#     age = request.json['age']

#     new_profile = profile(profileID, name, bio, gender, age, location)
#     ## retrieve image,
#     ## pass and store image in image microservice.
#     try:
#         db.session.add(new_profile)
#         db.session.commit()
#     except:
#         return jsonify({"message": "An error occurred creating the profile."}), 500

#     return jsonify(new_profile.json()), 201


if __name__ == "__main__":
    # app.run(port=5000,debug=True)
    print("Waiting for messages...")
    receiveOrder()