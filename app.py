import random
import string
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anonymous_campus_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

def generate_room_code():
    """Generates a random 6-character alpha-numeric room ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def home():
    # If a user visits the root address, redirect them to a brand new dynamic room
    return redirect(url_for('chat_room', room_id=generate_room_code()))

@app.route('/room/<room_id>')
def chat_room(room_id):
    # Renders the private chat environment
    return render_template('anon_chat.html', room_id=room_id)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    # Alerts existing peers in the room without reflecting back to the joiner
    emit('status', {'msg': "👤 An anonymous peer has joined the room."}, to=room, include_self=False)

@socketio.on('secure_msg')
def handle_secure_msg(data):
    # Blindly mirrors the cipher text back to all other room subscribers
    emit('receive_secure_msg', {'payload': data['payload']}, to=data['room'], include_self=False)

if __name__ == '__main__':
    socketio.run(app)