from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #Currently not in use, 1 migration needed for Agile marks.
from .models import Pokemon #Import models for database.
from .db import db

app = Flask(__name__)
app.config.from_object(Config)

#Database Intialisation.
db.init_app(app)
migrate = Migrate(app,db) #Currently no migration set up in current version

with app.app_context():
    Pokemon.initialise_database() #Initialises database - function checks to see if database currently exsists

from app import routes


