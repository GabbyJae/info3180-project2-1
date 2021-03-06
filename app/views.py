from app import app
from flask import request, redirect, url_for, render_template,jsonify,session,make_response,g
from models import Users,Posts,Follows,Likes
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename

from forms import SignUp,LoginIn,MakePost
from functools import wraps
import datetime
import os

import jwt

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        auth = request.headers.get('Authorization',None)

        if auth is None:
           return jsonify({'message':'Token is missing'})
        
        if auth.split()[0].lower() != "x-token" :
            return jsonify({'message':'Not a Token'})
        
        try:
            token  = auth.split()[1]
        except:
            return jsonify({'message':'Not a Token'})
            
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except jwt.DecodeError:
            return jsonify({'message':'Token is invalid'})
        except jwt.ExpiredSignature:
            return jsonify({'message':'Token is invalid'})
       
        g.current_user = data
        return func(*args, **kwargs)
    return wrapper
        
@app.route('/')
def home():
    return render_template("home.html")
    

@app.route('/api/auth/logout', methods=['POST'])
def api_auth_logout():
    return jsonify({'token':""})
    
@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    if not request.form['username']:
        return jsonify({'message':'No Username'}) 
    if  not request.form['password']:
         return jsonify({'message':'No Password'}) 
         
    username = request.form['username']
    password = request.form['password']
    
    try:
        user = Users.query.filter_by(username=username).first()
    except:
         user = None

    if not user:
       return jsonify({'message':'Invalid Username'}) 
    
    if check_password_hash(user.password,password):
        print("Yes")
        token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=45)},app.config['SECRET_KEY'])
    else:
        return jsonify({'message':'Invalid Password'}) 
    
    session["logged_in"] = True
    session["user_id"] = user.id
        
    return jsonify({'user_id':user.id,'token':token,'message':'sucess'})
   
    
@app.route('/api/user/register', methods=['POST'])
def api_user_register():
    
        
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        passwordraw = request.form['password']
        email = request.form['email']
        location = request.form['location']
        bio = request.form['biography']
        
        try:
            photo = request.files['photo']
            if firstname == "" or lastname == ""  or username == "" or email == "" or photo.filename == "" or bio =="" or location=="" or email=="":
                return jsonify({'message':'Required Field is missing'})
        except:
            return jsonify({'message':'Please submit a profile photo'})
            
        try:
            if Users.query.filter_by(username=username).first() :
                return jsonify({'message':'Username taken'})
        except:
             print('Ok')
             
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("./app/static/img",filename))

        password = generate_password_hash(passwordraw, method='sha256')
        
        user = Users(firstname=firstname,lastname=lastname,email=email,username=username,location=location,
                    password=password,biography=bio,photo=filename)
                    
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message':'Sucessfully Registered'})

@app.route('/api/posts', methods=['GET'])
@token_required
def api_posts():
   
    posts = Posts.query.all()
    
    if not posts:
        return jsonify({'message':'No post'})
            
    output = []
    
    for post in posts:
        postdata= {}
        
        poster =  Users.query.filter_by(id=post.user_id).first()
        likes  = Likes.query.filter_by(post_id=post.id).all()
        
        if not likes:
            postdata['no_of_likes'] = 0
        else:
            postdata['no_of_likes'] = len(likes)
            
        if not poster:
            postdata['username'] = "Anonymous"
            postdata['profile_pic'] = "anonymous.png"
        else:
             postdata['username'] = poster.username
             postdata['profile_pic'] = poster.profile_photo
             
        postdata['id'] = post.id
        postdata['user_id'] = post.user_id
        postdata['photo'] = post.photo
        postdata['caption'] = post.caption
        postdata['created_on'] = post.created_on[:-15]
        
        like = Likes.query.filter_by(user_id=int(g.current_user['user_id']),post_id=post.id).first()
        if like:
            postdata['liked'] = True
        else:
            postdata['liked'] = False
       
        output +=[postdata]
        
    return jsonify({'posts':output,'message':"All posts"})
    


@app.route('/api/users/<user_id>/posts', methods=['GET','POST'])
@token_required
def api_users_post(user_id):
    
    if(request.method == "GET"):
        posts = Posts.query.filter_by(user_id=int(user_id)).all()
        
        if not posts:
            return jsonify({'message':'No post'})
        
        output = []
    
        for post in posts:
            postdata= {}
            postdata['id'] = post.id
            postdata['user_id'] = post.user_id
            postdata['photo'] = post.photo
            postdata['caption'] = post.caption
            postdata['created_on'] = post.created_on[:-15]
            
            postdata['liked'] = False
            
            output +=[postdata]
        return jsonify({'posts':output,'message':"All posts"})
    else:
        
        jsonify({'message': request.form['caption']})
        
        try:
            photo = request.files['photo']
        except:
            jsonify({'message':'Photo is missing'})
        
        if  not request.form['caption']:
            return jsonify({'message':'No Caption'}) 
         
         
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("./app/static/img",filename))
        
        caption = request.form['caption']
        
        
        post = Posts(user_id=int(user_id),photo=filename,caption=caption)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({'message':'sucess'})
        
@app.route('/api/users/<user_id>/follow', methods=['POST'])
@token_required
def api_users_follow(user_id): 

        follower_id = g.current_user['user_id']

        follow = Follows(user_id=int(user_id),follower_id=int(follower_id))
        
        db.session.add(follow)
        db.session.commit()
        
        return jsonify({'message':'sucess'})

@app.route('/api/users/<user_id>', methods=['GET'])
@token_required
def api_users_user(user_id): 
        _user_ = Users.query.filter_by(id=int(user_id)).first()
        followers = Follows.query.filter_by(user_id=int(user_id)).all()
        posts = Posts.query.filter_by(user_id=int(user_id)).all()
        
        userinfo={}
        userinfo['no_of_followers'] = len(followers)
        userinfo['no_of_posts'] = len(posts)
        
        for f in followers:
            if(g.current_user['user_id'] == f.follower_id ):
                userinfo['no_follow'] = False
                
        if userinfo.get('no_follow',None) == None:
            userinfo['no_follow'] = True
        user={}
        user['firstname'] = _user_.firstname
        user['lastname'] = _user_.lastname
        user['profile_photo'] = _user_.profile_photo
        user['location'] = _user_.location
        user['created_on'] = _user_.joined_on.strftime('%d, %b %Y')
        user['biography'] = _user_.biography
        
        return jsonify({'user':user,'userinfo':userinfo,'message':'sucess'})
        

@app.route('/api/users/<post_id>/like', methods=['POST'])
@token_required
def api_posts_like(post_id):      
        like = Likes(user_id=g.current_user['user_id'],post_id=post_id)
        
        db.session.add(like)
        db.session.commit()
        
        return jsonify({'message':'sucess'})

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404  
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)

