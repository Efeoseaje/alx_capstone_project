from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


"""Initiate the Flask Module"""
app = Flask(__name__)
app.config['SECRET_KEY'] = '59e70fc843d568ca8365d516b9476882'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_schehduler.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routes