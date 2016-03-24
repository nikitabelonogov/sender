from flask import render_template, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import update
from flask.ext.socketio import SocketIO, emit

from app import app, login_manager, db, socketio
from models import User, Message, Dialog
import forms

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

def finddialogbetween(u1id, u2id):
    q1 = Dialog.query.filter(Dialog.user1_id == u1id).filter(Dialog.user2_id == u2id)
    q2 = Dialog.query.filter(Dialog.user1_id == u2id).filter(Dialog.user2_id == u1id)
    return q1.union(q2)
    
@app.route('/dialogwith/<int:userid>', methods=['GET'])
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
    dialogs = current_user.dialogs()
    dialogs = [d.__dict__  for d in dialogs]
    print dialogs
    return render_template('dialogs.html', title="Ur dialogs", dialogs=dialogs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Goodbye come again.")
    return redirect('/')