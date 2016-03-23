# from app.mode import Message
# print Message(1,2,'s').json()
from app import db
db.drop_all()
db.session.commit()