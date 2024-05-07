from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #Currently not in use, 1 migration needed for Agile marks.
from .db import db

app = Flask(__name__)
app.config.from_object(Config)

#Database Intialisation.
db.init_app(app)
migrate = Migrate(app,db) #Currently no migration set up in current version

from app import routes, models

with app.app_context():
    models.initialise_database() #Initialises database - function checks to see if database currently exsists



