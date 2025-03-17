from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager, login_user,UserMixin, login_required

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

lm = LoginManager(app)

from routes import *  

if __name__ == "__main__":
    app.run(debug=True)  
