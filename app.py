import random
import string
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anonymous_campus_secret_key'

# 🛠️ Explicitly tell Flask-SocketIO to use Python's built-in threading mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def home():
    return redirect(url_for('chat_room', room_id=generate_room_code()))

@app.route('/room/<room_id>')
def chat_room(room_id):
    return render_template('anon_chat.html', room_id=room_id)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': "👤 An anonymous peer has joined the room."}, to=room, include_self=False)

@socketio.on('secure_msg')
def handle_secure_msg(data):
    emit('receive_secure_msg', {'payload': data['payload']}, to=data['room'], include_self=False)

import os

if __name__ == '__main__':
    # Render automatically sets a 'PORT' environment variable. 
    # This reads that variable, or defaults to 10000 if running locally.
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
