from werkzeug.security import safe_str_cmp
from . import db
import datetime

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(500))
    firstname = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    email = db.Column(db.String(30))
    location = db.Column(db.String(50))
    biography = db.Column(db.String(500))
    profile_photo = db.Column(db.String(100))
    joined_on = db.Column(db.Date)
    
    def __init__(self,username,password,firstname,lastname,email,location,biography,photo):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = photo
        self.joined_on = datetime.datetime.now()
    
    def __str__(self):
        return "User id:",self.id

class Follows(db.Model):
    __tablename__ = "Follows"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)
    
    def __init__(self,user_id,follower_id):
        self.user_id = user_id
        self.follower_id = follower_id
    
class Posts(db.Model):
   __tablename__ = "Posts"
    
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer)
   photo = db.Column(db.String(500))
   caption = db.Column(db.String(500))
   created_on = db.Column(db.String(30))
   
   def __init__(self,user_id,photo,caption):
       self.user_id = user_id
       self.photo = photo
       self.caption = caption
       self.created_on = datetime.datetime.now()
       
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    
    def __init__(self,user_id,post_id):
        self.user_id = user_id
        self.post_id = post_id
    
def isfollowing(table,follower,following):
    flng = table.qutery.filter_by(username=follower).first().id
    flwr = table.qutery.filter_by(username=following).first().id
    for u in table.query.filter_by(follower=flng).all():
        if u == flwr:
            return True
    return False
    
def authenticate(table,username,password):
    user = table.query.filter_by(username=username)
    
    if user and safe_str_cmp(user.password.encode('utf-8'),password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return user_id.get(user_id, None)
