from flask import session, jsonify
from flask.ext.socketio import emit, join_room, leave_room
from flask_login import current_user

from app import socketio, db
from app.models import Message

@socketio.on('changeemoji', namespace='/index')
def changeemoji(message):
    current_user.emoji = int(message['msg'])
    db.session.commit()
    emit('changeemoji', {'msg': current_user.emoji})
    print 'left'
    
@socketio.on('join', namespace='/dialog')
def join(data):
    room = data['id']
    join_room(room)
    messages = Message.query.filter(Message.dialog_id == data['id'])
    messages = [m.json() for m in messages]
    emit('join', messages, broadcast=True, room=room)
    
@socketio.on('message', namespace='/dialog')
def join(data):
    room = data['dialog_id']
    message = Message(data['sender_id'], data['recipient_id'], data['text'])
    db.session.add(message)
    db.session.commit()
    emit('message', {'message':message.json(),'sender_id':data['sender_id']}, broadcast=True, room=room)