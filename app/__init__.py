from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'HJGFGHF^&%^&&*^&*YUGHJGHJF^%&YYHB'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/arrangement?charset=utf8mb4" % quote('dainyisheree')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app)

login = LoginManager(app)
