from flask import render_template, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import update
from flask.ext.socketio import SocketIO, emit

from app import app, login_manager, db, socketio
from models import User, Message, Dialog
import forms
from support import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

@app.errorhandler(404)
def not_found(error):
    flash('There is no such page.')
    return redirect('/')

@login_manager.unauthorized_handler
def unauthorized():
    flash("Authorize first.")
    return redirect('/signin')
    
@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template("index.html", title = 'Home')

@app.route('/', methods=['POST'])
def emojichange():
    current_user.emoji = unichr(int(request.data))
    db.session.commit()
    return render_template("index.html", title = 'Home')
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm(request.form)
    if current_user.is_authenticated:
        logout()
        return render_template('signup.html', title='Sing Up', form=form)    
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Hello, %s.' % current_user.username)
        flash('Nice to meet you.')
        return redirect('/')
    return render_template('signup.html', title='Sign Up', form=form)    
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = forms.SignInForm(request.form)
    if current_user.is_authenticated:
        logout()
        return render_template('signin.html', title='Sing In', form=form)
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter(User.username == form.username.data.lower()).first()
            login_user(user, remember=form.remember.data)
            flash('Hello again, ' + current_user.username)
            return redirect('/')
        else:
            flash('Wrong username or password.')
    return render_template('signin.html', title='Sign In', form=form)

@app.route('/users')
@login_required
def users():
    users = [u.json() for u in User.query.all()] 
    return render_template('users.html', title='Users', users=users)

@app.route('/user/<int:userid>')
@login_required
def user(userid):
    if current_user.id == userid:
        return redirect('/')
    user = User.query.filter(User.id == userid).first()
    return render_template('user.html', title=user.username, user=user)
    
def finddialogbetween(u1id, u2id):
    q1 = Dialog.query.filter(Dialog.user1_id == u1id).filter(Dialog.user2_id == u2id)
    q2 = Dialog.query.filter(Dialog.user1_id == u2id).filter(Dialog.user2_id == u1id)
    return q1.union(q2)
    
@app.route('/dialogwith/<int:userid>')
@login_required
def dialogwith(userid):
    user = User.query.filter(User.id == userid).first()
    if not user:
        flash('There is no user with id == ' + str(userid))
        return redirect('/users')
    q = finddialogbetween(current_user.id, user.id)
    if q.count() > 0:
        dialog = q.first()
    else:
        dialog = Dialog(current_user.id, user.id)
        db.session.add(dialog)
        db.session.commit()
    return render_template('dialogwith.html', title=user.username, user=user, dialog=dialog)

@app.route('/dialogs')
@login_required
def dialogs():
    dialogs = finddialogof(current_user)
    dialogs = [d.json() for d in dialogs]
    print dialogs
    return render_template('dialogs.html', title="Ur dialogs", dialogs=dialogs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Goodbye come again.")
    return redirect('/')
    
@app.route('/email', methods=['GET'])
@login_required
def emailget():
    form = forms.EmailSendForm()
    return render_template('email.html', title='Send email', form=form)
    
@app.route('/email', methods=['POST'])
@login_required
def emailpost():
    form = forms.EmailSendForm(request.form)
    
    import sendgrid

    client = sendgrid.SendGridClient("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")
    message = sendgrid.Mail()
    
    print(form.recipient.data)
    
    message.add_to(form.recipient.data)
    message.set_from(current_user.username + "@youremail.com")
    message.set_subject(form.subject.data)
    message.set_html(form.body.data)
    
    print(client.send(message))
    return redirect('/email')
    
    