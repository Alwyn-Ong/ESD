from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_profile'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class profile(db.Model):
    __tablename__ = 'profiledetails'

    profileID = db.Column(db.Integer(), primary_key=True)
    userID = db.Column(db.Integer(), unique=True, nullable=False)
    bio = db.Column(db.String(2083), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __init__(self, profileID, userID, bio, gender, age):
        self.profileID = profileID
        self.userID = userID
        self.bio = bio
        self.gender = gender
        self.age = age

    def json(self):
        return {"profileid": self.profileID, "userid": self.userID, "bio": self.bio, "gender": self.gender, "age": self.age}

## retrieve all profiles
@app.route("/allprofiles")
def get_all():
    #check if its only called by matching service then can call this service
    return jsonify({"all profiles": [profiles.json() for profiles in profile.query.all()]})    

#retrieve current profile (used as placeholder to edit)
@app.route("/profile/<int:userid>")
def find_by_userid(userid):
    userprofile = profile.query.filter_by(userID=userid).first()
    if userprofile:
        return jsonify(userprofile.json())
    return jsonify({"message": "profile not found"}), 404

#update profile
@app.route("/profile/<int:userid>/<string:attribute>",methods=['PUT'])
def update_profile(userid,attribute):
    userprofile = profile.query.filter_by(userID=userid).first()
    changecolumn = attribute
    # if userprofile:
    userprofile.changecolumn = 'changed'
    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred in updating the book."}), 500

    return "201"

#create profile 
@app.route("/profile", methods=['POST'])
def create_profile():
    userID = 7
    bio = request.json['bio']
    gender = request.json['gender']
    age = request.json['age']
if __name__ == "__main__":
    app.run(port=5000,debug=True)