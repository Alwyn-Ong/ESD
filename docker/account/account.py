from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/sglovelah_account'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)

class Account(db.Model):
    __tablename__ = 'account'

    accountid = db.Column (db.Integer, primary_key=True)
    email = db.Column (db.String(255),nullable=False)
    password = db.Column(db.Integer,nullable=False)

    def __init__(self, email, password, accountid= None):
        # As account id is auto incremental
        self.accountid = None
        self.email = email
        self.password = password

    def json(self):
        return {"accountid": self.accountid, "email": self.email, "password": self.password}


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
def authenticate_user():
    """
    Checks user password against that in Account DB

    Passes in data in the format 
    {
        "email":"",
        "password":""
    }

    Returns True/False

    Returns a message saying user does not exist if the user is not in the DB
    
    If email is in DB,
    Returns True or False, depending if the password matches that in the DB


    """
    data = request.get_json() 
    if (Account.query.filter_by(email=data["email"]).first()) == None:
        return jsonify({"message":"User with email '{}' does not exist.".format(data["email"])}), 400
    account = Account.query.filter_by(email=data["email"]).first()
    # account = Account(**data)

    if account.password == data["password"]:
        return json.dumps(account.accountid)

    # return json.dumps(account.password == data['password'])
    return jsonify({"message":"email or password is wrong."}), 404
        # return json.dumps(False)
    # return json.dumps(True)


@app.route("/register/",methods=['POST'])
def create_account():
    """
    Creates a user account in the Account DB.

    Passes in data in the format
    {
        "email"="",
        "password"=""
    }

    Returns 400 Error if email already exists

    Else, if there is an error creating, return error message

    Upon successful creation in account DB, return accountid.
    """
    data = request.get_json()
    
    
    if (Account.query.filter_by(email=data["email"]).first()) :
        return jsonify({"message":"An account with email '{}' already exists.".format(data["email"])}), 400

    account = Account(**data)

    try: 
        db.session.add(account)
        db.session.commit()
    except Exception as e:
        # print(e)
        return jsonify({f"message": "An error {e} occured creating the account."}), 500

    return json.dumps(account.accountid)
    # 201 is create

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
#Doesnt start up flask server if imported from elsewhere, can just run function



