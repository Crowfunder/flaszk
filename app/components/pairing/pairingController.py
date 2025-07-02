from flask import Blueprint, request, jsonify,flash,redirect,url_for
from flask import current_app, session
from app.database.models import Remote, db
from app.database.schema.schemas import RemoteSchema
from ..pairing.serverEvents import getSocketServer
import os, re, socket
from .pin.pinManager import pin as pin_class_instance
from ..utils.netUtils import checkIfHostUp
from .funcLibrary import validateIp

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
START_SERVER_ENDPOINT='/settings/start_server'
STOP_SERVER_ENDPOINT='/settings/stop_server'

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
    
    if not validateIp(ip):
        flash("Wrong IP address format given","error")
        return redirect(url_for('bp_client.settings'))
    if not port.isdigit() or not (1024 <= int(port) <= 65535):
        flash("Port must be a number between 1024 and 65535", "error")
        return redirect(url_for('bp_client.settings'))
    if not re.match(r"^\d{6}$", pin):
        flash("PIN must be a 6-digit number","error")
        return redirect(url_for('bp_client.settings'))
    
    if not checkIfHostUp(ip,port):
        flash("Host you are trying to connect is busy. Try again later.","warning")
        return redirect(url_for('bp_client.settings'))
    
    getSocketServer().initilaizeConnection(ip,port,pin)
    flash("Pairing started successfully",'info')
    return redirect(url_for('bp_client.settings'))

@bp.route(START_SERVER_ENDPOINT, methods=['GET'])
def startServer():
    port = os.getenv('FLASK_RUN_PORT')
    getSocketServer().run('0.0.0.0', port)
    import time
    time.sleep(0.25)
    flash("Server started successfully","info")
    my_ip = socket.gethostbyname_ex(socket.gethostname())[-1]
    my_port = port
    my_pin = pin_class_instance.get_pin()
    # Store in session
    session['pairing_info'] = {'my_ip': my_ip, 'my_port': my_port, 'my_pin': my_pin}
    return jsonify({'my_ip': my_ip, 'my_port': my_port, 'my_pin': my_pin}), 200

@bp.route(STOP_SERVER_ENDPOINT, methods=['POST'])
def stopServer():
    # Call your server disconnect logic
    socketServer = getSocketServer()
    del socketServer
    session.pop('pairing_info',None)
    flash("Server stopped successfully", "info")
    return redirect(url_for('bp_client.settings'))