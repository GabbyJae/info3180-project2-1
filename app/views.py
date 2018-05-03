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
        
        if auth.split()[0].lower() != "x-token":
            return jsonify({'message':'Not a Token'})
            
        token  = auth.split()[1]
        print(token)
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            
        except jwt.DecodeError:
            return jsonify({'message':'Token is invalid'})
        except jwt.ExpiredSignature:
            return jsonify({'message':'Token is invalid'})
       
        g.current_user = data
        print(data)
        return func(*args, **kwargs)
    return wrapper
        
@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/register')
def register():
    form = SignUp()
    return render_template("signup.html",form=form)
    
@app.route('/login')
def login():
    form = LoginIn()
    return render_template("login.html",form=form)
    
@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route('/myprofile')
def myprofile():
    return render_template("profile.html")
    
@app.route('/posts/new')
def post():
    form = MakePost()
    return render_template("createpost.html",form=form)

@app.route('/users/<user_id>')
def profiles():
    form = MakePost()
    return render_template("profiles.html",form=form)

@app.route('/users/profile')
def profile():
    form = MakePost()
    return render_template("profile.html",form=form)
    
@app.route('/posts/explore')
def explore():
    return render_template("posts.html")
    
@app.route('/api/auth/logout', methods=['POST'])
@token_required
def api_auth_logout():
    token = jwt.encode({},app.config['SECRET_KEY'])
    return jsonify({'token':token})
    
@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    auth = request.authorization
    
    if not request.form['username']:
        return jsonify({'message':'No Username'}) 
    if  not request.form['password']:
         return jsonify({'message':'No Password'}) 
         
    username = request.form['username']
    password = request.form['password']
    
    user = user.query.filter_by(username=username).first()
    
    if not user:
       return jsonify({'message':'Invalid Username'}) 
    
    if check_password_hash(user.password,password):
        token = jwt.encode({'user':user, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=45)},app.config['SECRET_KEY'])
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
        photo = request.files['photo']
        
        
        if firstname == "" or lastname == ""  or username == "" or email == "" or photo.filename == "":
            return jsonify({'message':'Required Field is missing'})
            
        try:
            if Users.query.filter_by(username=username).first() :
                return jsonify({'message':'Username taken'})
        except:
             print('Ok')
             
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("./app/static/img",filename))
        
        return jsonify({'message':'Sucessfully Registered'})
        
        password = generate_password_hash(passwordraw, method='sha256')
        
        user = Users(firstname=firstname,lastname=lastname,email=email,username=username,location=location,
                    password=password,biography=bio,photo=filename)
                    
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message':'Sucessfully Registered'})

@app.route('/api/post', methods=['GET'])
@token_required
def api_post():
   
    posts = Posts.query.all()
    
    output = []
    
    for post in posts:
        postdata= {}
        postdata['id'] = post.id
        postdata['user_id'] = post.user_id
        postdata['photo'] = post.photo
        postdata['caption'] = post.caption
        postdata['created_on'] = post.created_on
        output +=[postdata]
    return jsonify({'posts':output})

@app.route('/api/users/<user_id>/posts', methods=['GET','POST'])
@token_required
def api_users_post(user_id):
    
    if(request.method == "GET"):
        posts = Posts.query.filter_by(user_id=user_id).all()
        
        if not posts:
            return jsonify({'message':'No post'})
        
        output = []
    
        for post in posts:
            postdata= {}
            postdata['id'] = post.id
            postdata['user_id'] = post.user_id
            postdata['photo'] = post.photo
            postdata['caption'] = post.caption
            postdata['created_on'] = post.created_on
            output +=[postdata]
        return jsonify({'posts':output})
    else:
        data = request.get_json()
        photo = data['photo']
        caption = data['caption']
        
        post = Posts(user_id=user_id,photo=photo,caption=caption)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({'message':'Post added'})
        
@app.route('/api/users/<user_id>/follow', methods=['POST'])
@token_required
def api_users_follow(user_id): 
        user_id = g.current_user['id']
    
        data = request.get_json()
        follower_id = data['follower_id']
        
        follow = Follows(user_id=user_id,follower_id=follower_id)
        
        db.session.add(follow)
        db.session.commit()
        
        return jsonify({'message':'Followed'})

@app.route('/api/users/<post_id>/like', methods=['POST'])
@token_required
def api_posts_like(post_id):      
        like = Likes(user_id=current_user.id,post_id=post_id)
        
        db.session.add(like)
        db.session.commit()
        
        return jsonify({'message':'Liked'})
    
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)

