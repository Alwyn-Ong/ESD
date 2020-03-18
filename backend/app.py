from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils.functions import database_exists, create_database

app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/test2' 

db = SQLAlchemy(app)

engine = db.create_engine('mysql+mysqlconnector://root:@localhost:3306', creator=db) # connect to server
engine.execute("CREATE SCHEMA IF NOT EXISTS `Account`;") #create db
engine.execute("USE Account;") 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/Account' 
class Account(db.Model):
    accountId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

# engine = db.create_engine('mysql+pymysql://root:@localhost:3306', {}) # connect to server
# engine.execute("CREATE SCHEMA IF NOT EXISTS `Profile`;") #create db
# engine.execute("USE Profile;") 

# class Profile(db.Model):
#     profileId = db.Column(db.Integer, primary_key=True, autoincrement=False)
#     bio = db.Column(db.String(50))
#     gender = db.Column(db.String(50))
#     location = db.Column(db.String(50))
#     age = db.Column(db.Integer)

# engine = db.create_engine('mysql+pymysql://root:@localhost:3306', {}) # connect to server
# engine.execute("CREATE SCHEMA IF NOT EXISTS `Recommendation`;") #create db
# engine.execute("USE Recommendation;") 
# class Recommendation(db.Model):
#     recommendationId = db.Column(db.Integer, primary_key=True)
#     visitorId = db.Column(db.Integer)
#     visitedId = db.Column(db.Integer)
#     like = db.Column(db.Boolean)

# engine = db.create_engine('mysql+pymysql://root:@localhost:3306', encoding='latin1', echo=True) # connect to server
# engine.execute("CREATE SCHEMA IF NOT EXISTS `Image`;") #create db
# engine.execute("USE Image;") 

# class Image(db.Model):
#     imageId = db.Column(db.Integer, primary_key=True)
#     source = db.Column(db.String(50))

# class Notification(db.Model):
#     notificationId = db.Column(db.Integer, primary_key=True)
#     userId_1 = db.Column(db.Integer)
#     userId_2 = db.Column(db.Integer)
#     message = db.Column(db.String(300))

# class Chat(db.Model):
#     chatId = db.Column(db.Integer, primary_key=True)
#     matchId = db.Column(db.Integer)
#     chatHistory = db.Column(db.String(1000))
#     blackList = db.Column(db.Boolean)

# class Match(db.Model):
#     matchId = db.Column(db.Integer, primary_key=True)
#     userId_1 = db.Column(db.Integer)
#     userId_2 = db.Column(db.Integer)
#     ready_status = db.Column(db.Boolean)
#     ready_status = db.Column(db.Boolean)

# @app.route('/<string:email>/<string:password>')
# def account(email, password):
#     account = Account(email=email, password=password)
#     db.session.add(account)
#     db.session.commit()
#     return "<h1>New Account added!</h1>"



    



