from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, TextAreaField, validators

from models import User

class SignUpForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm', [validators.EqualTo('password', message='Passwords must match')])
    
    def validate(self):
        if Form.validate(self):
            if not User.query.filter_by(username=self.username.data.lower()).count():
                return True
        return False

class SignInForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Required()])
    remember = BooleanField('remember', default=False)
    
    def validate(self):
        if Form.validate(self):
            user = User.query.filter_by(username=self.username.data.lower()).first()
            print(user)
            if user:
                return user.check_password(self.password.data)
        return False
        
class SendMessageForm(Form):
    text = TextAreaField('text')
    
class EmailSendForm(Form):
    recipient = TextField('recipient', [validators.Email])
    subject   = TextField('subject')
    body      = TextAreaField('body')
    
    def validate(self):
        return Form.validate(self)