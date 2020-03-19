
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
# import sys
# import os
# import random
# import datetime

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.
import uuid
# import csv

app = Flask(__name__)
# Database name in this case is match
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/match'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


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
def add_match():
    """
    Creates a match in the Match DB.

    Passes in json data in the format
    {
        "id1"="",
        "id2"="",
    }

    Upon successful creation in account DB, return True.

    Else, if there is an error creating, return error message
    """
    data = request.get_json()
    id1 = data["id1"]
    id2 = data["id2"]

    # Checks if there are currently any existing matches in the database

    match_check = Match.query.filter_by(id1=id1, id2=id2).first()

    if match_check != None:
        return jsonify({"message": f"The match with id1:{id1} and id2:{id2} already exists."}), 500
    
    # if (Account.query.filter_by(username=data["username"]).first()) :
    #     return jsonify({"message":"A match with userid pair '{}' already exists.".format(data["username"])}), 400
    
    # elif (Account.query.filter_by(email=data["email"]).first()) :
    #     return jsonify({"message":"An account with email '{}' already exists.".format(data["email"])}), 400

    match = Match(**data)

    try: 
        db.session.add(match)
        db.session.commit()

        # Returns a MySQL row corresponding to the newly created match
        matchid = Match.query.filter_by(id1=id1,id2=id2).first()

        # Obtains the matchid from the row for processing
        matchid = matchid.matchid

        # Request from chat




    except Exception as e:
        # print(e)
        return jsonify({"message": f"An error {e} occured creating the match."}), 500

    return json.dumps(True)
    # 201 is create

@app.route("/match/",methods=['GET'])
def get_match_id():
    """
    Retrieves a match in the Match DB.

    Takes in a url in the format

    /match/?id1=123&id2=234
    
    If match exists:
    
    Returns the match id corresponding to id1 and id2

    Else, return error message match does not exist
    """
    id1 = request.args.get("id1")
    id2 = request.args.get("id2")
    
    matchid1 = Match.query.filter_by(id1 = id1, id2 = id2).first()
    matchid2 = Match.query.filter_by(id1 = id2, id2 = id1).first()

    if matchid1 != None:
        return jsonify(matchid1.matchid)
    elif matchid2 != None:
        return jsonify(matchid2.matchid)

    return jsonify({"message":f"A match with userid pair {id1} and {id2} does not exist."}) , 404

@app.route("/ready/",methods=['GET'])
def get_partner_ready_status():
    """
    Retrieves the ready status of the partner of an id in the Match DB.

    Takes in a url in the format

    /match/?id1=123&id2=234
    
    If match exists:
    
    Returns the ready status of the other partner

    Else, return error message match does not exist
    """
    id1 = request.args.get("id1")
    id2 = request.args.get("id2")
    
    matchid1 = Match.query.filter_by(id1 = id1, id2 = id2).first()
    matchid2 = Match.query.filter_by(id1 = id2, id2 = id1).first()

    if matchid1 != None:
        return json.dumps(matchid1.ready_status_2)
    elif matchid2 != None:
        return json.dumps(matchid2.ready_status_1)

    return jsonify({"message":f"A match with userid pair {id1} and {id2} does not exist."}) , 404

@app.route("/ready/",methods=['PUT'])
def update_partner_ready_status():
    """
    Updates the ready status of of an id in the Match DB
    The ready status of the id1 will be updated to true.

    Takes in a url in the format

    /match/?id1=123&id2=234
    
    If match exists:
    
    Updates the ready status and returns success of update.

    Else, return error message match does not exist
    """
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


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # print("This is " + os.path.basename(__file__) + ": creating an order...")
    # order = create_order("sample_order.txt")
    # send_order(order)
    # receiveOrder()
#    print(get_all())
#    print(find_by_order_id(3))
