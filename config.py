import os

class config: 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/academiahydra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1234'