from flask import Flask
import flask_sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "itsasecret"
app.config['SQLALCHEMY_DATABAS_URI'] = "sqlite:///UserData.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = flask_sqlalchemy.SQLAlchemy(app)

from app import views