from flask import render_template,redirect,request,flash,url_for,session
from dihealthapp import app
from dihealthapp.models import db,User,Payment,Meal,Diet,Admin


@app.route('/ajax/diet/delete/',methods=['POST','GET'])
def ajax_delete():
    id=request.form.get('id')
    
    db.session.query(Diet).filter(Diet.id==id).delete()
    
    db.session.commit()
    redirect('/admin/diet/')
    return 'deleted'

@app.route('/ajax/subscribe/cancel/',methods=['POST','GET'])
def subscribe_cancel():
    id=request.form.get('id')
    pay=db.session.query(Payment).filter(Payment.id==id).first()
    
    pay.status="cancelled"
    pay.user.status='disabled'
    db.session.commit()
    redirect('/admin/subscription/')
    return 'cancelled'

@app.route('/ajax/subscribe/disable/',methods=['POST','GET'])
def subscriber_disable():
    id=request.form.get('id')
    pay=db.session.query(Payment).filter(Payment.id==id).first()
    
    pay.user.status="disabled"
    db.session.commit()
    redirect('/admin/subscription/')
    return 'disabled'


@app.route('/ajax/payment/delete/',methods=['POST','GET'])
def payment_delete():
    id=request.form.get('id')
    pay=db.session.query(Payment).filter(Payment.id==id).delete()
    
    db.session.commit()
    redirect('/admin/payments/')
    return 'deleted'

@app.route('/ajax/user/activate/',methods=['POST','GET'])
def user_activate():
    id=request.form.get('id')
    user=db.session.query(User).filter(User.id==id).first()
    
    user.status="active"
    db.session.commit()
    redirect('/admin/users/')
    return 'activated'

@app.route('/ajax/user/disable/',methods=['POST','GET'])
def user_disable():
    id=request.form.get('id')
    user=db.session.query(User).filter(User.id==id).first()
    
    user.status="disabled"
    db.session.commit()
    redirect('/admin/users/')
    return 'disabled'

@app.route('/ajax/payment/cancel/',methods=['POST','GET'])
def payment_cancel():
    id=request.form.get('id')
    pay=db.session.query(Payment).filter(Payment.id==id).first()
    
    pay.status="cancelled"
    
    db.session.commit()
    redirect('/admin/payments/')
    return 'cancelled'

@app.route('/ajax/payment/activate/',methods=['POST','GET'])
def payment_activate():
    id=request.form.get('id')
    pay=db.session.query(Payment).filter(Payment.id==id).first()
    
    pay.status="completed"
    
    db.session.commit()
    redirect('/admin/payments/')
    return 'activated'

@app.route('/ajax/meal/pend/',methods=['POST','GET'])
def meal_pend():
    id=request.form.get('id')
    meal=db.session.query(Meal).filter(Meal.id==id).first()
    
    meal.status="pending"
    
    db.session.commit()
    redirect('/admin/meal/')
    return 'Pended!'

@app.route('/ajax/meal/approve/',methods=['POST','GET'])
def meal_approve():
    id=request.form.get('id')
    meal=db.session.query(Meal).filter(Meal.id==id).first()
    
    meal.status="approved"
    
    db.session.commit()
    redirect('/admin/meal/')
    return 'approved!'

@app.route('/ajax/add/diet/',methods=['POST','GET'])
def add_diet():
    diet=request.form.get('diet')
    newdiet= Diet(name=diet)
    
    db.session.add(newdiet)
    db.session.commit()
    return 'New Diet added successfully!'