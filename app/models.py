from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from app import db
def finddialogbetween(u1id, u2id):
    q1 = Dialog.query.filter(Dialog.user1_id == u1id).filter(Dialog.user2_id == u2id)
    q2 = Dialog.query.filter(Dialog.user1_id == u2id).filter(Dialog.user2_id == u1id)
    return q1.union(q2)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(70), nullable=False)
    emoji = db.Column(db.Integer, nullable=False, default=128515)
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, username, password):
        self.username = username.lower()
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.id
    
    def json(self):
        return {"id":self.id,"username":self.username,"emoji":self.emoji}
        

class Dialog(db.Model):
    __tablename__ = 'dialogs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user1    = db.relationship(User, foreign_keys='Dialog.user1_id')
    user2    = db.relationship(User, foreign_keys='Dialog.user2_id')
    
    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
    
    def json(self):
        return {"id":self.id,"user1":self.user1.json(),"user2":self.user2.json()}

class Message(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String())
    timestamp = db.Column(db.DateTime(), server_default=db.func.now())
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender    = db.relationship(User, foreign_keys='Message.sender_id')
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient    = db.relationship(User, foreign_keys='Message.recipient_id')
    dialog_id = db.Column(db.Integer, db.ForeignKey('dialogs.id'), nullable=False)
    dialog    = db.relationship(Dialog, foreign_keys='Message.dialog_id')
    

    def __init__(self, sender_id, recipient_id, text):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.dialog_id = finddialogbetween(sender_id, recipient_id).first().id
        
    def json(self):
        return {"sender_id":self.sender_id,"recipient_id":self.recipient_id,"text":self.text,"timestamp":str(self.timestamp),"sender":self.sender.json()}