from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/test2' 
db = SQLAlchemy(app)

class Account(db.Model):
    accountId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Profile(db.Model):
    profileId = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(1000))
    location = db.Column(db.String(200))
    birtday = db.Column(db.Date)
    gender = db.Column(db.String(10))
    accountId = db.Column(db.Integer, unique=True)


if __name__ == '__main__':
    manager.run()