from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

db = SQLAlchemy()
bcrypt = Bcrypt()
mongo = PyMongo()