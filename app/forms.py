from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import StringField,TextAreaField,SubmitField,PasswordField
from wtforms import validators

class SignUp(FlaskForm):
    username = StringField('Username',[validators.Required("Must have a user name")])
    password = StringField('Password',[validators.Required("Must have a password")])
    firstname = StringField('Firstname',[validators.Required("Must have a first name")])
    lastname = StringField('Lastname',[validators.Required("Must have a last name")])
    email = StringField('Email',[validators.Required("Must have an email")])
    location = StringField('Location')
    biography = TextAreaField('Biography')
    photo = FileField("Photo",validators = [FileRequired(),FileAllowed(['jpg','png','jpeg'])])    
    submit = SubmitField("Add Register")

class LoginIn(FlaskForm):
    username = StringField('Username',[validators.Required("Must have a username")])
    password = PasswordField('Password',[validators.Required("Must have a password")])
    
class MakePost(FlaskForm):
    Caption = TextAreaField('Caption')
    photo = FileField("Photo",validators = [FileRequired(),FileAllowed(['jpg','png','jpeg'])])