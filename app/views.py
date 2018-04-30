from app import app
from flask import request, redirect, url_for, render_template,jsonify,make_response
from models import Users,Posts,Follows,Likes
from app import db
from werkzeug.security import generate_password_hash,check_password_hash


from forms import SignUp,LoginIn,MakePost
from functools import wraps
import datetime

import jwt

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        
        auth = request.headers.get('x-token-access',None)
        
        if auth is not None:
            token = request.headers['x-token-access']
        else:
            return jsonify({'message':'Token is missing'})
            
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message':'Token is invalid'})
       
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
    return render_template("posts.html",form=form)
    
@app.route('/api/auth/login', methods=['POST'])
def api_auth_logout():
    token = jwt.encode({},app.config['SECRET_KEY'])
    return jsonify({'token':token.decode('UTF-8')})
    
@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    auth = request.authorization
    
    if not auth or not auth.password or not auth.username:
        return make_response("Could not verify", 401 , {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    username = auth.username
    password = auth.password
    
    user = user.query.filter_by(username=username).first()
    
    if not user:
        make_response("Could not verify", 401 , {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    if check_password_hash(user.password,password):
        token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=45)},app.config['SECRET_KEY'])
        
        return jsonify({'token':token.decode('UTF-8')})
    return make_response("Could not verify", 401 , {'WWW-Authenticate': 'Basic realm="Login required"'})
    
@app.route('/api/user/register', methods=['POST'])
@token_required
def api_user_register(current_user):
        data  = request.get_json()
        
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        passwordraw = data['password']
        email = data['email']
        location = data['location']
        bio = data['bio']
        photo = data['photo']
        
        try:
            if Users.query.filter_by(username=username).first() :
                return jsonify({'result':'Username taken'})
        except:
             print('ok')
         
        if firstname is None or lastname is None  or username is None or email is None:
            return jsonify({'message':'Required Field is missing'})
        
        password = generate_password_hash(passwordraw, method='sha256')
        
        user = Users(firstname=firstname,lastname=lastname,email=email,username=username,location=location,
                    password=str(password),biography=bio,photo=photo)
                    
        db.session.add(user)
        #db.session.commit()
        
        return jsonify({'message':'Sucessfully Registered'})

@app.route('/api/post', methods=['GET'])
@token_required
def api_post(current_user):
   
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
def api_users_post(current_user,user_id):

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
def api_users_follow(current_user,user_id):      
        data = request.get_json()
        follower_id = data['follower_id']
        
        follow = Follows(user_id=user_id,follower_id=follower_id)
        
        db.session.add(follow)
        db.session.commit()
        
        return jsonify({'message':'Followed'})

@app.route('/api/users/<post_id>/like', methods=['POST'])
@token_required
def api_posts_like(current_user,post_id):      
        like = Likes(user_id=current_user.id,post_id=post_id)
        
        db.session.add(like)
        db.session.commit()
        
        return jsonify({'message':'Likes'})
    
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)

