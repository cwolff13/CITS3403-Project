from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from .db import db

app = Flask(__name__)
app.config.from_object(Config)

#Database Intialisation.
db.init_app(app)
migrate = Migrate(app,db) #Currently no migration set up in current version

# Login Management
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

with app.app_context():
    models.initialise_database() #Initialises database - function checks to see if database currently exsists



