from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tmp.db'
socketio = SocketIO(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routs, events, models

db.create_all()
