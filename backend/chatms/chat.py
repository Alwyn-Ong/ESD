from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class chatdetails(db.Model):
    __tablename__ = 'chatdetails'

    matchID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    chatroom_ID = db.Column(db.VARCHAR(50), nullable=False)

    def __init__(self, matchID, chatroom_ID, blacklisted = False):
        self.matchID = matchID
        self.blacklisted = blacklisted
        self.chatroom_ID= chatroom_ID

    def json(self):
        return {"matchID": self.matchID, "blacklisted": self.blacklisted, "chatroom_ID": self.chatroom_ID}

class chatroom_details(db.Model):
    __tablename__ = 'chatroom_details'

    chatroom_ID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    chatroom_name = db.Column(db.VARCHAR(50), nullable=False)
    serveraddress = db.Column(db.VARCHAR(50), nullable=False)
    Used = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, chatroom_ID, chatroom_name, serveraddress, Used):
        self.chatroom_ID = chatroom_ID
        self.chatroom_name = chatroom_name
        self.serveraddress = serveraddress
        self.Used = Used

    def json(self):
        return {"chatroom_ID": self.chatroom_ID, "chatroom_name": self.chatroom_name, "serveraddress": self.serveraddress, "Used": self.Used}

class chatroom1(db.Model):
    __tablename__ = 'chatroom1'

    messageID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    msg = db.Column(db.VARCHAR(500), nullable=False)

    def __init__(self, userID, msg, created_on=None, messageID=None):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom2(db.Model):
    __tablename__ = 'chatroom2'

    messageID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    msg = db.Column(db.VARCHAR(500), nullable=False)

    def __init__(self, userID, msg, created_on=None, messageID=None):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom3(db.Model):
    __tablename__ = 'chatroom3'

    messageID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    msg = db.Column(db.VARCHAR(500), nullable=False)

    def __init__(self, userID, msg, created_on=None, messageID=None):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroomfour(db.Model):
    __tablename__ = 'chatroom4'

    messageID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    msg = db.Column(db.VARCHAR(500), nullable=False)

    def __init__(self, userID, msg, created_on=None, messageID=None):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom5(db.Model):
    __tablename__ = 'chatroom5'

    messageID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer(), nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    msg = db.Column(db.VARCHAR(500), nullable=False)

    def __init__(self, userID, msg, created_on=None, messageID=None):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}


## create new row in chatdetails
@app.route("/createchat", methods=['POST'])
def createchat(matchID=1):
    # hardcode matchID but retrieve from matchMS.
    desired_room_status = 0
    chatroom = chatroom_details.query.filter_by(Used=desired_room_status).first()
    newchatroom_id = chatroom.chatroom_ID
    newchatrow = chatdetails(matchID,newchatroom_id)
    try:
        db.session.add(newchatrow)
        db.session.commit()
        updateoccupancy(newchatroom_id)
    except:
        return jsonify({"message": "An error occurred creating the profile."}), 500

    return jsonify(newchatrow.json()), 201

def updateoccupancy(id):
    chatroom = chatroom_details.query.filter_by(chatroom_ID=id).first()
    chatroom.Used = 1
    db.session.commit()
    return '201'

@app.route("/blacklist", methods=['PUT'])
def blacklistuser():
    ##hardcoded matchID
    matchID = 1
    chatprofile = chatdetails.query.filter_by(matchID=matchID).first()
    chatprofile.blacklisted = 1
    db.session.commit()
    return "201"

## get IP address of which server to join based on matchID
@app.route("/getchataddress")
def getchataddress(matchID=5):
    ##hardcoded matchID
    chatprofile = chatdetails.query.filter_by(matchID=matchID).first()
    chatroomID = chatroom_details.query.filter_by(chatroom_ID=chatprofile.chatroom_ID).first()
    chatroomserveraddress = chatroomID.serveraddress

    return jsonify({"chatserver": chatroomserveraddress})

##update chat logs everytime i send message    
@app.route('/updatechatlogs', methods=['POST'])
def updatechatlogs():
    ## hardcode matchID and userID (From session) and msg
    matchID = 5
    userID = 3
    msg = 'hello hello testing database'
    chatprofile = chatdetails.query.filter_by(matchID=matchID).first()
    chatroomID = chatprofile.chatroom_ID
    chatroomprofile = chatroom_details.query.filter_by(chatroom_ID=chatroomID).first()
    chatroomname = chatroomprofile.chatroom_name
    
    if chatroomname == 'chatroom1':
        newmsg = chatroom1(userID,msg)
    elif chatroomname == 'chatroom2':
        newmsg = chatroom2(userID,msg)
    elif chatroomname == 'chatroom3':
        newmsg = chatroom3(userID,msg)
    elif chatroomname == 'chatroom4':
        newmsg = chatroomfour(userID,msg)
    elif chatroomname == 'chatroom5':
        newmsg = chatroom5(userID,msg)
    try:
        db.session.add(newmsg)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the profile."}), 500

    return jsonify(newmsg.json()), 201

#
if __name__ == "__main__":
    app.run(port=5000,debug=True)