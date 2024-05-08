#Separating db initialisation from init.py to prevent circular import error. Done differently inside lab example couldn't figure out smarter way. 
#Can probably be fixed later.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()