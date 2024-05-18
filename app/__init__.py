from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import *
from .db import db

# Login Management
login = LoginManager()
login.login_view = 'login'

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    #Database Intialisation.
    db.init_app(app)
    login.init_app(app)
    
    from app.blueprints import main
    app.register_blueprint(main)
    
    with app.app_context():
        from app.models import initialise_database
        initialise_database() #Initialises database - function checks to see if database currently exsists
    return app
   
   
   



