import os
from datetime import datetime
import secrets
import random
import json
import requests
from flask import render_template,redirect,request,flash,url_for,session
from sqlalchemy import func,and_
from werkzeug.security import generate_password_hash,check_password_hash
from dihealthapp import app
from dihealthapp.forms import SignupForm,LoginForm
from dihealthapp.models import db,User,Subscription,Payment,Admin,Meal,Diet


@app.after_request
def after_request(response):
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return response


@app.route('/')
def index():
    return render_template('index.html',key=app.config['PAYSTACK_KEY'])

@app.route('/login/',methods=['POST','GET'])
def login():
    form=LoginForm()
    if request.method=='POST':
        #retrieve form data
        email=request.form.get('email')
        password=request.form.get('password')
        usertype=request.form.get('usertype')
        if usertype=="1":
            admin=db.session.query(Admin).filter(Admin.email==email).first()
            if admin:
                hashed_password=admin.password
                check=check_password_hash(hashed_password,password)
                if check:
                    session['admin_id']=admin.id
                    flash('Log in sucessful')
                    return redirect('/admin/home/')
                else:
                    flash('Incorrect password')
                    return redirect('/login/')
            else:
                flash('Invalid e-mail')
                return redirect('/login/')
        elif usertype=="2":
            user=db.session.query(User).filter(User.email==email).first()
            if user:
                hashed_password=user.password
                check=check_password_hash(hashed_password,password)
                if check:
                    session['user_id']=user.id
                    flash('Log in sucessful')
                    print(user.diet_id)
                    if user.diet_id == None:
                        return redirect('/diet/goal/')
                    else:
                        return redirect('/home/')
                else:
                    flash('Incorrect password')
                    return redirect('/login/')
                    
            else:
                flash("email is invalid")
                return redirect('/login/')
        else:
            flash("please select a usertype")
            return redirect('/login/')
    
    return render_template("login.html",form=form)

@app.route('/home/')
def home():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    user_all=db.session.query(User).all()
    meal_all=db.session.query(Meal).all()
    diet_all=db.session.query(Diet).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/user/home.html',user=user,admin=admin,user_all=user_all,meal_all=meal_all,diet_all=diet_all)

@app.route('/diet/goal/',methods=['POST','GET'])
def diet_goal():
    admin_id=session.get('admin_id')
    admin=db.session.query(User).filter(User.id==admin_id).first()
    if request.method=="GET":
        user_id=session.get('user_id')
        user=db.session.query(User).filter(User.id==user_id).first()
        
        diets=db.session.query(Diet).all()
        return render_template("user/needs.html",user=user,diets=diets,admin=admin)
    else:
        user_id=session.get('user_id')
        user=db.session.query(User).filter(User.id==user_id).first()
        need=int(request.form.get('needs'))
        user.diet_id=need
        
        db.session.commit()
        return redirect("/home/")
    
    


@app.route('/signup/',methods=['POST','GET'])
def center_register():
    form=SignupForm()
    if request.method == 'GET':
        return render_template('signup.html',form=form)
    else:
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        phone=request.form.get('phone')
        email=request.form.get('email')
        gender=request.form.get('gender')
        pass1=request.form.get('password')
        pass2=request.form.get('confirmpassword')
        
        # validate email,name&password
        if email==''or pass1=='' or firstname=='' or lastname=='':
            flash('Your Firstname,Lastname,Email and Password can not be blank','error')
            return redirect(url_for('center_register'))
        elif pass1 != pass2:
            flash('The two passwords must match','error')
            return redirect(url_for('center_register'))
        else:
            hatched=generate_password_hash(pass1)
            user=User(firstname=firstname,lastname=lastname,email=email,gender=gender,phone=phone,password=hatched)
            try:
                
                db.session.add(user)
                db.session.commit()
        
                flash('Welcome,an account has been created for you')
                return redirect("/login/")
            except:
                flash('The email is already in use,choose another please')
                return redirect(url_for('center_register'))
            
@app.route('/logout/')
def logout():
    if session.get('user_id')!=None:
        session.pop('user_id')
        if session.get('ref')!=None:
            session.pop('ref')
        flash('You are now logged out')
        return redirect('/login/')
    elif session.get('admin_id')!=None:
        session.pop('admin_id')
        flash('You are now logged out')
        return redirect('/login/')


@app.route('/profile/')
def profile():
    user_id=session.get('user_id')
    user=db.session.query(User).filter(User.id==user_id).first()
    
    return render_template('user/user_profile.html',user=user)

@app.route('/diet/suggest/daily/')
def diet_suggest():
    user_id=session.get('user_id')
    user=db.session.query(User).filter(User.id==user_id).first()
    if user.status=="active":
        time=datetime.now()
        breakfast_start= datetime.strptime("7:00:00", "%H:%M:%S")
        lunch_start= datetime.strptime("12:00:00", "%H:%M:%S")
        dinner_start=datetime.strptime("18:00:00", "%H:%M:%S")
        if  time > dinner_start:
            meal=db.session.query(Meal).filter(Meal.diet_id==user.diet_id).filter(Meal.status=='approved').filter(Meal.time=="dinner").order_by(func.random()).first()
        elif time > lunch_start:
            meal=db.session.query(Meal).filter(Meal.diet_id==user.diet_id).filter(Meal.status=='approved').filter(Meal.time=="lunch").order_by(func.random()).first()
        elif time > breakfast_start:
            meal=db.session.query(Meal).filter(Meal.diet_id==user.diet_id).filter(Meal.status=='approved').filter(Meal.time=="breakfast").order_by(func.random()).first() 
        else:
            meal=None
        return render_template('user/diet_suggest.html',user=user,meal=meal)
    else:
        return redirect('/subscribe/')
    


# @app.route('/diet/monthly/mealplan/')
# def meal_plan():
#     user_id=session.get('user_id')
#     user=db.session.query(User).filter(User.id==user_id).first()
#     if user.status=="active":
#         return render_template('user/meal_plan.html',user=user)
#     else:
#         return redirect('/subscribe/')

@app.route('/subscribe/')
def subscribe():
    user_id=session.get('user_id')
    user=db.session.query(User).filter(User.id==user_id).first()
    
    return render_template('user/subscribe.html',user=user)

@app.route('/subscribe/regular/')
def subscribe_confirm():
    user_id=session.get('user_id')
    user=db.session.query(User).filter(User.id==user_id).first()
    
    if user_id:
        ref=random.randint(10000000000000000000,90000000000000000000)
        ref_no=f"FA{ref}"
        session["ref"]=ref_no
        payment=Payment(user_id=user_id,subscription_id=1,ref=ref_no)
        db.session.add(payment)
        db.session.commit()
        payment.status='processing'
        db.session.commit()
        return render_template('user/confirm_sub.html',user=user,pay=payment)
    else:
        flash('you need to log in to make payment')
        return redirect('/login/')
    
@app.route('/subscribe/premium/')
def subscribe_premium():
    user_id=session.get('user_id')
    user=db.session.query(User).filter(User.id==user_id).first()
    if user_id:
        ref=random.randint(10000000000000000000,90000000000000000000)
        ref_no=f"FA{ref}"
        session["ref"]=ref_no
        payment=Payment(user_id=user_id,subscription_id=2,ref=ref_no)
        payment.status='processing'
        db.session.commit()
        return render_template('user/confirm_sub.html',user=user,pay=payment)
    else:
        flash('you need to log in to make payment')
        return redirect('/login/')
    

@app.route('/subscribe/paystack/', methods=['POST'])
def subscribe_paystack():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    ref=session.get('ref')
    if ref:
        url= "https://api.paystack.co/transaction/initialize"
        headers={"Content-Type":"application/json","Authorization": app.config['PAYSTACK_KEY']}
        payment=db.session.query(Payment).filter(Payment.status=="processing").filter(Payment.ref==ref).filter(Payment.user_id==user_id).first()
        data={"email":user.email,"amount":payment.subscription.amount*100,"reference":payment.ref,"callback_url":"http://127.0.0.1:5000/subscribe/landing/"}
        resp_json=requests.post(url,headers=headers,data=json.dumps(data))
        resp_dict=resp_json.json()
        print(resp_dict)
        if resp_dict and resp_dict.get('status')==True:
            auth_url=resp_dict['data']['authorization_url']
            return redirect(auth_url)
        else:
            pay=db.session.query(Payment).filter(Payment.user_id==user_id and Payment.status=="processing" and Payment.ref==ref).first()
            pay.status="cancelled"
            session.pop('ref')
            db.session.commit()
            flash("payment did not go through")
            return redirect ('/subscribe/')
    else:
        pay=db.session.query(Payment).filter(Payment.user_id==user_id and Payment.status=="processing" and Payment.ref==ref).first()
        pay.status="cancelled"
        session.pop('ref')
        db.session.commit()
        flash("payment could not be completed")
        redirect('/subscribe/')
        
@app.route('/subscribe/landing/')
def subscribe_success():
    ref=session.get('ref')
    trxref=request.args.get('trxref')
    payment=db.session.query(Payment).filter(Payment.ref==ref).first()
    if (ref != None) and (ref==trxref):
        url=f"https://api.paystack.co/transaction/verify/{ref}"
        headers={"Authorization":"Bearer sk_test_4c7b242342502220c7b1a2c538d74e8034dec554"}

        resp_json=requests.get(url,headers=headers)
        resp_dict=resp_json.json()
        pay=Payment.query.filter(Payment.ref==ref).first()
        print(resp_dict)
        if resp_dict['data']['status']=="success":
            payment.status="completed"
            session.pop('ref')
            user_id=session.get('user_id')
            user=db.session.query(User).filter(User.id==user_id).first()
            user.status="active"
            if payment.subscription_id=="2":
                user.subscription_id="2"
                db.session.commit()
            else:
                user.subscription_id="1"
                db.session.commit()
                
            flash('Subcription updated! you can now enjoy our services')
            return redirect('/diet/suggest/daily/')
        else:
            session.pop('ref')
            flash('Donation was not successful')
            payment.status="cancelled"
            db.session.commit()
            return redirect('/subscribe/')
    else:
        session.pop('ref')
        payment.status="cancelled"
        db.session.commit()
        flash('Please start your subscribtion process again')
        return redirect('/subscribe/')
    

@app.route("/user/<id>/update/", methods=['POST','GET'])
def update_profile (id):
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==id).first()
   
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    if request.method=='POST':
        phone=request.form.get('phone')
        pic=request.files.get('pic')
        bio=request.form.get('bio')
        
        original_filename=pic.filename
        if original_filename !="":
            ext=os.path.splitext(original_filename)
            extension=ext[1]
            
            newfilename=secrets.token_hex(10)
            pic.save("dihealthapp/static/user_image/"+newfilename+extension)
            user.profilepic=f"user_image/{newfilename}{extension}"
            user.phone=phone
            user.bio=bio
            
            db.session.commit()
            
            flash("your profile has been updated!")
            return redirect('/profile/')
    return render_template("user/update.html", user=user,admin=admin)
    





