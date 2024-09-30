import os
import secrets
import random
import json
import requests
from flask import render_template,redirect,request,flash,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from dihealthapp import app
from dihealthapp.forms import SignupForm,LoginForm
from dihealthapp.models import db,User,Payment,Meal,Diet,Admin


@app.after_request
def after_request(response):
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return response

@app.route('/admin/home/')
def admin_home():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    user_all=db.session.query(User).all()
    meal_all=db.session.query(Meal).all()
    diet_all=db.session.query(Diet).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/home.html',user=user,admin=admin,user_all=user_all,meal_all=meal_all,diet_all=diet_all)

@app.route('/admin/users/')
def admin_user():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    users=db.session.query(User).all()
    
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    
    return render_template('admin/users.html',user=user,users=users,admin=admin)


@app.route('/admin/diet/')
def admin_diet():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    diet_all=db.session.query(Diet).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/diet.html',user=user,admin=admin,diets=diet_all)
    
    
@app.route('/admin/meal/')
def admin_meal():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    meal_all=db.session.query(Meal).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/meal_plans.html',user=user,admin=admin,meals=meal_all)

@app.route('/admin/profile/')
def admin_profile():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/admin_profile.html',user=user,admin=admin)

@app.route("/admin/<id>/update/", methods=['POST','GET'])
def admin_update_profile (id):
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==id).first()
    if request.method=='POST':
        phone=request.form.get('phone')
        pic=request.files.get('pic')
        
        original_filename=pic.filename
        if original_filename !="":
            ext=os.path.splitext(original_filename)
            extension=ext[1]
            
            newfilename=secrets.token_hex(10)
            pic.save("dihealthapp/static/user_image/"+newfilename+extension)
            admin.profilepic=f"user_image/{newfilename}{extension}"
            admin.phone=phone
            
            db.session.commit()
            
            flash("your profile has been updated!")
            return redirect('/admin/profile/')
    return render_template("admin/update.html", user=user,admin=admin)
    
    
    
@app.route('/admin/subscription/')
def admin_subscribe():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    payment_all=db.session.query(Payment).filter(Payment.status=="completed").all()
    
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/subscribe.html',user=user,admin=admin,payment_all=payment_all)

@app.route('/admin/payments/')
def admin_payments():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    payment_all=db.session.query(Payment).all()

    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/payments.html',user=user,admin=admin,payment_all=payment_all)


@app.route('/admin/meal/<id>/')
def meal_selected(id):
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    meal_all=db.session.query(Meal).filter(Meal.diet_id==id).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/meal_selected.html',user=user,admin=admin,meals=meal_all)

@app.route('/admin/meal/update/',methods=['POST','GET'])
def meal_update():
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    diets=db.session.query(Diet).all()

    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    if request.method=='POST':
        diet=request.form.get('diet')
        app=request.form.get('appert')
        main=request.form.get('main')
        desert=request.form.get('desert')
        drink=request.form.get('drink')
        note=request.form.get('note')
        time=request.form.get('time')
        prop=request.form.get('prop')
        
        meal=Meal(diet_id=diet,appetizer=app,maincourse=main,desert=desert,drink=drink,additional_note=note,time=time,added_by=admin_id,proportion=prop)
        
        db.session.add(meal)
        db.session.commit()
    
        flash('meal updated successfully')
        return redirect("/admin/meal/")
    return render_template('/admin/meal_update.html',user=user,admin=admin,diets=diets)


@app.route('/admin/meal/edit/<id>/',methods=['POST','GET'])
def meal_edit(id):
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
    diets=db.session.query(Diet).all()
    
    meal=db.session.query(Meal).filter(Meal.id==id).first()
    
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    if request.method=='POST':
        diet=request.form.get('diet')
        app=request.form.get('appert')
        main=request.form.get('main')
        desert=request.form.get('desert')
        drink=request.form.get('drink')
        note=request.form.get('note')
        time=request.form.get('time')
        prop=request.form.get('prop')
        
        
        
        meal.diet_id=diet
        meal.appetizer=app
        meal.maincourse=main
        meal.desert=desert
        meal.drink=drink
        meal.additional_note=note
        meal.time=time
        meal.added_by=admin_id
        meal.proportion=prop
        
        
        db.session.commit()

        flash('meal edited successfully')
        return redirect("/admin/meal/")
    return render_template('/admin/meal_edit.html',user=user,admin=admin,meal=meal,diets=diets)


@app.route('/admin/meal/added/<id>/')
def meal_addedby(id):
    user_id=session.get("user_id")
    user=db.session.query(User).filter(User.id==user_id).first()
   
    meal_all=db.session.query(Meal).filter(Meal.added_by==id).all()
    
    admin_id=session.get("admin_id")
    admin=db.session.query(Admin).filter(Admin.id==admin_id).first()
    return render_template('/admin/meal_selected.html',user=user,admin=admin,meals=meal_all)