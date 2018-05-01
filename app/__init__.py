from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "itsasecret"

#For Heroku database which I pushed 
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://jpksuqatakngxa:52a669bd612ed3c38b8dde53dbd94a1baa592d66303dfcb2ed6c6119cf2e2689@ec2-107-20-249-68.compute-1.amazonaws.com:5432/dbtpli1m01eqh"

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://stephan542:Project_2@localhost/UsersData"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from app import views 