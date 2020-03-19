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


@socketio.on('message')
def handleMessage(msg):
    print('Message:' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)