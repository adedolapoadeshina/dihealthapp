from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,SelectField,RadioField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class SignupForm(FlaskForm):
    firstname= StringField('First Name',validators=[DataRequired(message="Kindly fill out the first name field!"),Length(max=50)])
    lastname= StringField('Last Name',validators=[DataRequired(message="Kindly fill out the last name field!"),Length(max=50)])
    phone=StringField('Phone Number',validators=[DataRequired(message="Please input a valid phone number"),Length(max=15)])
    email=StringField('Email',validators=[DataRequired(message="Kindly input an email address"),Email(message="Please input a valid email")])
    gender=SelectField('Gender',choices=[('female','Female'),('male','Male')],validators=[DataRequired(message="Please input your gender")])
    password=PasswordField('Password',validators=[DataRequired(message="Password field cannot be empty")])
    confirmpassword=PasswordField('Confirm Password',validators=[DataRequired(message="Confirm Password field cannot be empty"),EqualTo('password', message="Password mismatch")])
    submit=SubmitField('REGISTER')

class LoginForm(FlaskForm):
    
    email=StringField('Email',validators=[DataRequired(message="Kindly input an email address"),Email(message="Please input a valid email")])
    password=PasswordField('Password',validators=[DataRequired(message="Password field cannot be empty")])
    usertype=SelectField('Select Usertype',choices=[('1','Admin'),('2','User')],validators=[DataRequired(message="Kidly select usertype")])

    
    submit=SubmitField('LOG IN')
    
    
    
    

class Meta:
    csrf = True
    csrf_time_limit = 7200