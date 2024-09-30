from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diet(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    diet_id=db.Column(db.String(255),nullable=True)
    
    #relationship
    meal = db.relationship('Meal',back_populates='diet')
    

class Admin(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False,unique=True)
    phone = db.Column(db.String(20),nullable=True)
    password = db.Column(db.String(255),nullable=False)
    profilepic=db.Column(db.String(255),nullable=True,default="static/user_image/profilephoto.png")
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    
    #relationship
    


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    firstname = db.Column(db.String(255),nullable=False)
    lastname = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False,unique=True)
    gender=db.Column(db.Enum('female','male'), nullable=False)
    phone = db.Column(db.String(20),nullable=True)
    password = db.Column(db.String(255),nullable=False)
    bio = db.Column(db.Text,nullable=True)
    profilepic=db.Column(db.String(255),nullable=True,default="user_image/profilephoto.png")
    diet_id = db.Column(db.Integer,db.ForeignKey('diet.id'),nullable=True)
    subscription_id = db.Column(db.Integer,db.ForeignKey('subscription.id'),nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    status =db.Column(db.Enum('active','disabled'), server_default=("disabled"))
    

    # set relationship
    subscription = db.relationship('Subscription',back_populates='user')
    review = db.relationship('Review',back_populates='user')
    diet = db.relationship('Diet',backref='user_diet')
    user_record = db.relationship('UserRecord',back_populates='user')
    
    


class Record(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    
    user_record = db.relationship('UserRecord',back_populates='record')
    
    
class UserRecord(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    record_id = db.Column(db.Integer,db.ForeignKey('record.id'),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    
    # set relationship
    record = db.relationship('Record',back_populates='user_record')
    user = db.relationship('User',back_populates='user_record')
    
    
class Meal(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    diet_id = db.Column(db.Integer,db.ForeignKey('diet.id'),nullable=False)
    appetizer = db.Column(db.Text,nullable=False)
    maincourse = db.Column(db.Text,nullable=False)
    desert = db.Column(db.Text,nullable=False)
    drink=db.Column(db.Text,nullable=False)
    additional_note=db.Column(db.Text,nullable=True)
    time=db.Column(db.Enum('breakfast','lunch','dinner'),nullable=False)
    added_by=db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    proportion= db.Column(db.Text,nullable=False)
    status = db.Column(db.Enum('approved','pending'),server_default=("pending"))
    # set relationship
    diet = db.relationship('Diet',back_populates='meal')
    admin = db.relationship('Admin',backref='admin')
    review = db.relationship('Review',back_populates='meal')


class Subscription(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    amount = db.Column(db.Integer,nullable=False)   
    
    # set relationship
    payment = db.relationship('Payment',back_populates='subscription')
    user = db.relationship('User',back_populates='subscription')
    
    

class Payment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    payment_date = db.Column(db.DateTime,default=datetime.utcnow)
    ref=db.Column(db.String(200))  
    status = db.Column(db.Enum('completed','pending','cancelled','processing'),server_default=("pending"))
    subscription_id = db.Column(db.Integer,db.ForeignKey('subscription.id'),nullable=False)
    
    # set relationship
    subscription = db.relationship('Subscription',back_populates='payment')
    user = db.relationship('User',backref='payment')

    





class Review(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    meal_id = db.Column(db.Integer,db.ForeignKey('meal.id'),nullable=False)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'),nullable=False)
    comment = db.Column(db.Text,nullable=False)
    status = db.Column(db.Enum('active','disabled'),server_default=("active"))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    # set relationship
    user = db.relationship('User',back_populates='review')
    meal = db.relationship('Meal',back_populates='review')
    admin = db.relationship('Admin',backref='review')









































