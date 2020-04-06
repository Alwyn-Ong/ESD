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

    profileID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    name = db.Column(db.VARCHAR(50), nullable=False)
    bio = db.Column(db.String(2083), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    location = db.Column(db.VARCHAR(255), nullable=False)

    def __init__(self, profileID, name, bio, gender, age, location):
        self.profileID = profileID
        self.name = name
        self.bio = bio
        self.gender = gender
        self.age = age
        self.location = location

    def json(self):
        return {"profileid": self.profileID, "name":self.name, "bio": self.bio, "gender": self.gender, "age": self.age, "location":self.location}

## retrieve all profiles
@app.route("/allprofiles")
def get_all():
    #check if its only called by matching service then can call this service
    return jsonify({"all profiles": [profiles.json() for profiles in profile.query.all()]})    

#retrieve current profile (used as placeholder to edit)
@app.route("/profile/<int:profileid>",methods=['GET'])
def find_by_userid(profileid):
    userprofile = profile.query.filter_by(profileID=profileid).first()
    if userprofile:
        return jsonify(userprofile.json())
    return jsonify({"message": "profile not found"}), 404

#update profile
@app.route("/updateprofile/<int:profileID>",methods=['PUT'])
def update_profile(profileID):
    userprofile = profile.query.filter_by(profileID=profileID).first()
    #update the entire profile
    data = request.get_json()
    location = data['location']
    userprofile.location = location
    bio = data['bio']
    userprofile.bio = bio
    gender = data['gender']
    userprofile.gender = gender
    age = data['age']
    userprofile.age = age
    name = data['name']
    userprofile.name = name

    try:
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred in updating the profile."}), 500

    return "201"

#create profile 
@app.route("/profile", methods=['POST'])
def create_profile():
    ##profileID not suposed to be given
    profileID = request.json['profileID']
    ##hardcoded for now
    name = request.json['name']
    location = request.json['location']
    bio = request.json['bio']
    gender = request.json['gender']
    age = request.json['age']

    new_profile = profile(profileID, name, bio, gender, age, location)
    # return new_profile.json()
    ## retrieve image,
    ## pass and store image in image microservice.
    try:
        db.session.add(new_profile)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the profile."}), 500

    return jsonify(new_profile.json()), 201


if __name__ == "__main__":
    app.run(port=2000,debug=True)
