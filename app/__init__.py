from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = '59e70fc843d568ca8365d516b9476882'

# Create an SQLAlchemy engine to connect to your MySQL database
engine = create_engine('mysql://root:chelsea008@localhost/event_scheduler')

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Define your model
Base = declarative_base()
salt = bcrypt.gensalt()


from app import routes
