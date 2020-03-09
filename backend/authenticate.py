from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# JWT Config https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension (JWT Config)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'account'

    accountid = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(255),nullable=False)
    email = db.Column (db.String(255),nullable=False)
    password = db.Column(db.Integer,nullable=False)

    def __init__(self, username, email, password, accountid= None):
        # As account id is auto incremental
        self.accountid = None
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return {"accountid": self.accountid, "username": self.username, "email": self.email, "password": self.password}


# @app.route("/book")
# def get_all():
#     return jsonify({"books": [book.json() for book in Book.query.all()]})

# @app.route("/book/<string:isbn13>")
# def find_by_isbn13(isbn13):
#     book = Book.query.filter_by(isbn13=isbn13).first()
#     if book:
#         return jsonify(book.json())
#     return jsonify({"message":"Book not found"}), 404

@app.route("/login/", methods=['POST'])
def login():
    """
    Checks user password against that in Account DB

    Passes in data in the format 
    {
        "username":"",
        "password":""
    }
    Returns a message saying user does not exist if the user is not in the DB
    
    If username is in DB,
    Returns True or False, depending if the password matches that in the DB
    """

    # Data Validation (JWT Config)
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400


    data = request.get_json()
    if (Account.query.filter_by(username=data["username"]).first()) == None:
        return jsonify({"message":"User '{}' does not exist.".format(data["username"])}), 400
    account = Account.query.filter_by(username=data["username"]).first()
    # account = Account(**data)

    # Checks if either username or pw is wrong (JWT config)
    if username != account.username or password != account.password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable (JWT config)
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

    # return json.dumps(account.password == data['password'])
        # return jsonify({"message":"Username or password is wrong."}), 404
        # return json.dumps(False)
    # return json.dumps(True)

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/register/",methods=['POST'])
def create_account():
    """
    Creates a user account in the Account DB.

    Passes in data in the format
    {
        "username"="",
        "email"="",
        "password"=""
    }

    Returns 400 Error if username already exists

    Else, if there is an error creating, return error message

    Upon successful creation in account DB, return True.
    """
    data = request.get_json()
    
    if (Account.query.filter_by(username=data["username"]).first()) :
        return jsonify({"message":"An account with username '{}' already exists.".format(data["username"])}), 400
    
    elif (Account.query.filter_by(email=data["email"]).first()) :
        return jsonify({"message":"An account with email '{}' already exists.".format(data["email"])}), 400

    account = Account(**data)

    try: 
        db.session.add(account)
        db.session.commit()
    except Exception as e:
        # print(e)
        return jsonify({f"message": "An error {e} occured creating the book."}), 500

    return json.dumps(True)
    # 201 is create

if __name__ == '__main__':
    app.run(port=5000, debug=True)
#Doesnt start up flask server if imported from elsewhere, can just run function



