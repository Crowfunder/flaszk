from flask import Blueprint
from flask import current_app
from flask_socketio import SocketIO

    # Activating socket
socketio = SocketIO(current_app)



bp = Blueprint('bp_pairing', __name__)