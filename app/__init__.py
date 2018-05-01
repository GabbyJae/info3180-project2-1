from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "itsasecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://stephan542:Project_2@localhost/UsersData"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from app import views 