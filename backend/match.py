
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

# For HTTP Calls
import requests


# import sys
# import os
# import random
# import datetime

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
# import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.
# import uuid
# import csv

app = Flask(__name__)
# Database name in this case is match
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_match'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)

chatURL = 'http://localhost:5009'


class Match(db.Model):
    __tablename__ = 'match'

    matchid = db.Column(db.Integer, primary_key=True)
    id1 = db.Column(db.Integer)
    id2 = db.Column(db.Integer)
    ready_status_1 = db.Column(db.Boolean, default=False)
    ready_status_2 = db.Column(db.Boolean, default=False)

    def __init__(self, id1, id2, ready_status_1=0, ready_status_2=0, matchid=None):
        self.matchid = matchid
        self.id1 = id1
        self.id2 = id2
        self.ready_status_1 = ready_status_1
        self.ready_status_2 = ready_status_2

    def json(self):
        return {"matchid": self.matchid, "id1": self.id1, "id2": self.id2, "ready_status_1": self.ready_status_1, "ready_status_2": self.ready_status_2}

@app.route("/match/",methods=['POST'])
def add_match(id1 = None,id2 = None):
    """
    Creates a match in the Match DB.

    Passes in json data in the format
    {
        "id1"="",
        "id2"=""
    }

    If there is an error creating in account DB, return error message
    
    Else, after adding to account DB, gets the matchid of the newly created match,
    and creates a corresponding row in chat DB, using HTTP Call.

    If there is an error creating in chat DB, return error message.
    Else, returns success message.

    """

    # Gets variables if done through http call

    # Implemented to account for function call from match_receiver

    if id1 == None and id2 == None:
        data = request.get_json()
        id1 = data["id1"]
        id2 = data["id2"]

    # Checks if there are currently any existing matches in the database
    match_check = Match.query.filter_by(id1=id1, id2=id2).first()
    match_check_2 = Match.query.filter_by(id1=id2, id2=id1).first()

    
    # Returns error message if the match already exists
    if match_check != None or match_check_2 != None:
        return jsonify({"message": f"The match with id1:{id1} and id2:{id2} already exists."}), 500
    
    # Adds to match db if match does not exist
    match = Match(id1,id2)
    
    try: 
        db.session.add(match)
        db.session.commit()

        # Returns a MySQL row corresponding to the newly created match
        matchid = Match.query.filter_by(id1=id1,id2=id2).first()

    except Exception as e:
        return jsonify({"message": f"An error {e} occured creating the match."}), 500

    # Obtains the newly created matchid for creating row in chat
    matchid = matchid.matchid

    # Creates a new rom in chat, through HTTP Call.
    create_chat_url = chatURL + "/createchat"

    # Prepares POST message for sending
    message = {"matchid":int(matchid)}

    # Sends request with message as JSON
    r = requests.post(create_chat_url,json=message)

    # Saves response
    result = r.json()

    # Returns error message or success message accordingly
    try:
        error = result["message"]
        return jsonify({"message":error})

    except KeyError:
        return jsonify({"message":"Successful creation into DB"}), 200
        # 201 is create



@app.route("/match/<int:id1>/<int:id2>",methods=['GET'])
def get_match_id(id1,id2):
    """
    Retrieves a matchid from the Match DB.

    Takes in a url in the format

    /match/id1/id2

    If match exists:
    
    Returns the match id corresponding to id1 and id2

    Else, return error message match does not exist
    """
    # id1 = request.args.get("id1")
    # id2 = request.args.get("id2")
    
    matchid1 = Match.query.filter_by(id1 = id1, id2 = id2).first()
    matchid2 = Match.query.filter_by(id1 = id2, id2 = id1).first()

    if matchid1 != None:
        return jsonify(matchid1.matchid)
    elif matchid2 != None:
        return jsonify(matchid2.matchid)

    return jsonify({"message":f"A match with userid pair {id1} and {id2} does not exist."}) , 404

@app.route("/ready/<int:matchid>/<int:vid>")
def get_partner_ready_status(matchid,vid):
    """
    Retrieves the ready status of the partner of an id in the Match DB.

    Takes in a url in the format

    /match/1/2
    
    If match exists:
    
    Returns the ready status of the other partner

    Else, return error message match does not exist
    """
    # id1 = request.args.get("id1")
    # id2 = request.args.get("id2")
    
    matchid1 = Match.query.filter_by(matchid = matchid, id1 = vid).first()
    matchid2 = Match.query.filter_by(matchid = matchid, id2 = vid).first()

    if matchid1 != None:
        return json.dumps(matchid1.ready_status_2)
    elif matchid2 != None:
        return json.dumps(matchid2.ready_status_1)

    return jsonify({"message":f"A match with matchID does not exist."}) , 404

@app.route("/allmatches/<int:id>",methods=['GET'])
def get_all_matches(id):
    """
    Retrieves all the matches of an id in the Match DB. For use in calling chat

    Takes in a url in the format

    /match/1
    
    If match exists:
    
    Returns the ready status of the other partner

    Else, return error message match does not exist
    """
    # id1 = request.args.get("id1")
    # id2 = request.args.get("id2")
    
    # First checks for matches with user as id1
    matchids = Match.query.filter_by(id1 = id)

    # Subsequently checks for matches with user as id2
    matchids2 = Match.query.filter_by(id2 = id)

    if matchids == None and matchids2 == None:

        # Returns error message if user is in neither id1 nor id2
        return jsonify({"message":f"User {id} is not found."})
    
    # Returns a list of users that are matched with user as id1 and id2
    return jsonify({"matchids": [matchid.id2 for matchid in matchids] + [matchid2.id1 for matchid2 in matchids2]})

@app.route("/ready/<int:matchid>/<int:userid>",methods=['PUT'])
def update_partner_ready_status(matchid,userid):
    """
    Updates the ready status of of an id in the Match DB
    The ready status of the id1 will be updated to true.

    Takes in a url in the format

    /match/?id1=123&id2=234
    
    If match exists:
    
    Updates the ready status and returns success of update.

    Else, return error message match does not exist
    """
    matchid1 = Match.query.filter_by(matchid = matchid, id1 = userid).first()
    matchid2 = Match.query.filter_by(matchid = matchid, id2 = userid).first()
    if matchid1 != None:
        matchid1.ready_status_1 = 1
    else:
        matchid1.ready_status_2 = 1

    try:
        db.session.commit()
        return jsonify({"message": f"The update status of {id1} has been updated!"})
    except Exception as e:
        return jsonify({"message": f"An error {e} occured updating the database."})

    data = request.get_json()
    id1 = data["id1"]
    id2 = data["id2"]
    
    matchid1 = Match.query.filter_by(id1 = id1, id2 = id2).first()
    matchid2 = Match.query.filter_by(id1 = id2, id2 = id1).first()

    if matchid1 != None:
        matchid1.ready_status_1 = 1

        try:
            db.session.commit()
            return jsonify({"message": f"The update status of {id1} has been updated!"})
        except Exception as e:
            return jsonify({"message": f"An error {e} occured updating the database."})
    
    elif matchid2 != None:
        matchid2.ready_status_2 = 1

        try:
            db.session.commit()
            return jsonify({"message": f"The update status of {id2} has been updated!"})
        except Exception as e:
            return jsonify({"message": f"An error {e} occured updating the database."})   

    return jsonify({"message":f"A match with userid pair {id1} and {id2} does not exist."}) , 404

@app.route("/checkreadystatus/<int:matchid>")
def checkreadystatus(matchid):
    matchids = Match.query.filter_by(matchid = matchid).first()
    if matchids != None:
        return jsonify({"id1":matchids.id1,"status_1":matchids.ready_status_1,"id2":matchids.id2,"status_2":matchids.ready_status_2})
    # if matchids.ready_status_1 == 1 and matchids.ready_status_2 == 1:
    #     return jsonify({"message": "success"})
    # else:
    #     return jsonify({"message":"fail"})


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(port=7007, debug=True)
    # print("This is " + os.path.basename(__file__) + ": creating an order...")
    # order = create_order("sample_order.txt")
    # send_order(order)
    # receiveOrder()
#    print(get_all())
#    print(find_by_order_id(3))
