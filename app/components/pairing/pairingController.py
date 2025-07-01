from flask import Blueprint, request, jsonify
from flask import current_app
from flask_socketio import SocketIO
from .serverEvents import serverEventsHandler
from app.database.models import Remote, db
from app.database.schema.schemas import RemoteSchema
from ..pairing.serverEvents import getSocketServer


bp = Blueprint('bp_pairing', __name__)



def importRemote(address, port, secret):
    
    # Check if remote has been indexed
    existingRemote = Remote.query.filter_by(address=address, port=port).first()
    
    # Remote was not indexed before
    if not existingRemote:
        existingRemote = Remote(
            address=address,
            port=port,
            secret=secret
        )
        db.session.add(existingRemote)
    else:
        # Optionally update the secret if needed
        existingRemote.secret = secret
    db.session.commit()


REMOTE_ADD_ENDPOINT = '/remotes/add'
START_PAIRING_ENDPOINT='/settings/start_pairing'

# TODO: Secure with @login_required !!!!
@bp.route(REMOTE_ADD_ENDPOINT, methods=['POST'])
def remoteAdd():
    data = request.get_json()
    address = data.get('address')
    port = data.get('port')
    secret = data.get('secret')
    if not address or not port or not secret:
        return jsonify({'error': 'Missing required fields'}), 400
    importRemote(address, port, secret)
    return 'added', 200

@bp.route(START_PAIRING_ENDPOINT,methods=['POST'])
def startPairing():
    ip=request.form['ip_address']
    port=request.form['port']
    pin=request.form['pin']
    

    return 'pairing started', 200