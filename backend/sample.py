from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
##pip3 install pyrebase

name = 'testing'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class Book(db.Model):
    __tablename__ = 'book'

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}


@app.route("/book")
def get_all():
    return jsonify({"books": [book.json() for book in Book.query.all()]})


@app.route("/book/<string:isbn13>")
def find_by_isbn13(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        return jsonify(book.json())
    return jsonify({"message": "Book not found"}), 404


@app.route("/book/<string:isbn13>",methods=['POST'])
def create_book(isbn13):
    if (Book.query.filter_by(isbn13=isbn13).first()):
        return jsonify({"message": "A book with isbn13 '{}' already exists.".format(isbn13)}), 400

    data = request.get_json()
    book = Book(isbn13, **data)

    try:
        db.session.add(book)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the book."}), 500

    return jsonify(book.json()), 201


if __name__ == "__main__":
    app.run(port=5000,debug=True)
#doesnt start up flask server if imported from elsewhere.


# debug is True means dont need restart app if there are changes.
# if __name__ == "__m"