from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_images'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class image(db.Model):
    __tablename__ = 'images'

    profileID = db.Column(db.Integer(), primary_key=True, autoincrement=False)
    profileImage = db.Column(db.String(2083), nullable=False)

    def __init__(self, profileID, profileImage):
        self.profileID = profileID
        self.profileImage = profileImage

    def json(self):
        return {"profileid": self.profileID, "profileImage": self.profileImage)

## retrieve all profiles
@app.route("/upload" , methods= ['POST'] )
def upload():
    #check if its only called by matching service then can call this service
    file = request.files['inputFile']

    return file.filename


if __name__ == "__main__":
    app.run(port=5000,debug=True)