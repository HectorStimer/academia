from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from config import config
import os

class config: 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/academiahydra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1234'


db = SQLAlchemy()

app = Flask(__name__)


db.init_app(app)

from routes import *  

if __name__ == "__main__":
    app.run(debug=True)  
