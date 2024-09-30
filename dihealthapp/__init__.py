from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dihealthapp.models import db
from dotenv import load_dotenv

migrate=Migrate() #initializing Migrate
csrf=CSRFProtect() #initializing csrf

def create_app():
    app=Flask(__name__,instance_relative_config=True,static_folder="static",template_folder="templates")
    app.config.from_pyfile('config.py',silent=True)
    db.init_app(app)
    migrate.init_app(app,db)
    csrf.init_app(app)
    
    return app

app=create_app()


from dihealthapp import admin_routes,routes,ajax_routes,forms