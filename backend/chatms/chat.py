from flask import Flask
from flask_socketio import SocketIO, send
from flask_cors import CORS
from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

class chatdetails(db.Model):
    __tablename__ = 'chatdetails'

    matchID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    blacklisted = db.Column(db.Boolean, nullable=False)
    chatroom_name = db.Column(db.VARCHAR(50), nullable=False)

    def __init__(self, matchID, blacklisted, chatroom_name):
        self.matchID = matchID
        self.blacklisted = blacklisted
        self.chatroom_name= chatroom_name

    def json(self):
        return {"matchID": self.matchID, "blacklisted": self.blacklisted, "chatroom_name": self.chatroom_name}

class chatroom_details(db.Model):
    __tablename__ = 'chatroom_details'

    def __init__(self, chatroom_ID, chatroom_name, serveraddress, Used):
        self.chatroom_ID = chatroom_ID
        self.chatroom_name = chatroom_name
        self.serveraddress = serveraddress
        self.Used = Used

    def json(self):
        return {"chatroom_ID": self.chatroom_ID, "chatroom_name": self.chatroom_name, "serveraddress": self.serveraddress, "Used": self.Used}

class chatroom_one(db.Model):
    __tablename__ = 'chatroom1'

    def __init__(self, messageID, userID, created_on, msg):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom_two(db.Model):
    __tablename__ = 'chatroom2'

    def __init__(self, messageID, userID, created_on, msg):
        self.messageID = messageID
        self.userID = userID,
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom_three(db.Model):
    __tablename__ = 'chatroom3'

    def __init__(self, messageID, userID, created_on, msg):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom_four(db.Model):
    __tablename__ = 'chatroom4'

    def __init__(self, messageID, userID, created_on, msg):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}

class chatroom_five(db.Model):
    __tablename__ = 'chatroom5'

    def __init__(self, messageID, userID, created_on, msg):
        self.messageID = messageID
        self.userID = userID
        self.created_on = created_on
        self.msg = msg

    def json(self):
        return {"messageID": self.messageID, "userID": self.userID, "created_on": self.created_on, "msg": self.msg}




@socketio.on('message')
def handleMessage(msg):
    print('Message:' + msg)
    send(msg, broadcast=True)



if __name__ == '__main__':
    socketio.run(app)