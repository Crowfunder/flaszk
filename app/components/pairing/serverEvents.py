from flask import request, Blueprint
from flask import current_app as app
from flask_socketio import *
from .funcLibrary import *
from .modularEquations import *
import os
import socketio
import time
from .pairingConfig import *


bp = Blueprint('bp_server', __name__)

class serverEventsHandler():
    def __init__(self,socketIO, flask_app):
        self.flask_app = flask_app
        self.socketIO= socketIO
        self.sio=socketio.Client()
        self.sid_dict_server={}
        self.sid_dict_client={}
        self.register_handlers_pairing_server()
        self.register_handlers_pairing_client()
    
    def run(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port
        self.socketIO.run(app,f'host={self.server_ip}',f'port={self.server_port}') #odpalenie nasłuchiwania serwera na danym ip i porcie
            
    #####################################################################
    # S E R V E R 
    #####################################################################
            
    def register_handlers_pairing_server(self):
        self.socketIO.on_event('connect', self.on_connect)
        self.socketIO.on_event('verificate_PIN', self.on_verificate_PIN)
        self.socketIO.on_event('estabilish_secret_start', self.on_estabilish_secret_start)
        self.socketIO.on_event('estabilish_secret_end', self.on_estabilish_seceret_end)
        self.socketIO.on_event('disconnect', self.on_disconnect)
        
    def on_connect(self):
        app.logger.info("%s Server connected with new client",request.sid)
        print(self.server_port)
        self.socketIO.emit('server_welcome',{'port':str(self.server_port)},to=request.sid)
        
    def on_verificate_PIN(self,data):
        ip_address=data.get('ip_address')
        port=data.get('port')
        PIN=data.get('pin')
        if is_PIN_correct(PIN):
            self.socketIO.emit('is_PIN_correct',{'msg': 'Right PIN given'},to=request.sid)
            self.sid_dict_server[request.sid]=connectionParameters(stage=1, ip_address=ip_address,port=port,is_paired=False)
            app.logger.info("%s Server PIN successfully verified",request.sid)  
        else:
            app.logger.info("%sPIN veirfication unsuccessfull",request.sid)
            self.socketIO.send('disconnect_client', to=request.sid)
            self.socketIO.disconnect(request.sid)
                
    def on_estabilish_secret_start(self,data):
        if self.sid_dict_server[request.sid].stage == 1:
            coded_nr=int(data.get('coded_nr'))
            self.sid_dict_server[request.sid].p=int(data.get('p'))
            p=self.sid_dict_server[request.sid].p
            generated_nr=generateExponent(p,False)
            self.sid_dict_server[request.sid].secret_nr=generated_nr
            
            msg=modularExponentation(coded_nr,generated_nr,p)
            self.socketIO.emit('server_secret_response',{'msg': str(msg)},to=request.sid)
            
            self.sid_dict_server[request.sid].stage=2
            app.logger.info("%sFirst Shamir response succesfull",request.sid)
        else:
            app.logger.info("%sFirst Shamir response unsuccesfull",request.sid)
            self.socketIO.send('disconnect_client', to=request.sid)
            self.socketIO.disconnect(request.sid)
            del self.sid_dict_server[request.sid]
            

    def on_estabilish_seceret_end(self,data):
        if self.sid_dict_server[request.sid].stage==2:
            coded_nr=int(data.get('data'))
            secret_nr=self.sid_dict_server[request.sid].secret_nr
            p=self.sid_dict_server[request.sid].p
            secret_inverse=inverseModular(secret_nr,p)
            secret=modularExponentation(coded_nr,secret_inverse,p)
            
            record=self.sid_dict_server[request.sid]
            createRemote(record.ip_address,record.port,str(secret))
            
            self.socketIO.emit('secret_recieved_successfully',to=request.sid)
            self.sid_dict_server[request.sid].is_paired=True
        else:
            self.socketIO.send('disconnect_client', to=request.sid)
            # self.socketIO.disconnect(request.sid)
            del self.sid_dict_server[request.sid]
        
    def on_disconnect(self, data):
        app.logger.info("%s Server disconnected", request.sid)
        del self.sid_dict_server[request.sid]
        
    #####################################################################
    # C L I E N T 
    #####################################################################
        
    def register_handlers_pairing_client(self):
        # self.sio.on('connect',self.on_server_welcome)
        self.sio.on('server_welcome', self.on_server_welcome)
        self.sio.on('is_PIN_correct', self.on_is_PIN_correct)
        self.sio.on('server_secret_response',self.on_server_secret_response)
        self.sio.on('disconnect_client', self.on_disconnect_client)
        self.sio.on('secret_recieved_successfully',self.on_secret_recieved_successfully)
    
    def initilaizeConnection(self,server_ip_address,port, client_app):
        self.client_app = client_app
        app.logger.info('mango')
        self.server_ip=server_ip_address
        self.port=port
        if not self.sio.connected:
            self.sio.connect(f'http://{server_ip_address}:{port}', namespaces=['/']) # defined port --> to be decided later
        else:
            self.sio.disconnect()
            time.sleep(0.25)
            self.sio.connect(f'http://{server_ip_address}:{port}', namespaces=['/'])
    
    def on_server_welcome(self,data):
        app.logger.info('mango')
        port=data.get('port')
        self.sid_dict_client[self.sio.sid]=connectionParametersClient(ip_address=self.server_ip,port=port)
        self.sio.sleep(0.25)
        if self.sio.connected:
            self.sio.emit('verificate_PIN', {'ip_address':self.server_ip,'pin' : 1234,'port':str(self.server_port)})
        else:
            print('xyz')
        
    def on_is_PIN_correct(self,data):
        msg=data.get('msg')
        p=generateExponent(PRIME_GENERATING_LIMIT,True)
        self.sid_dict_client[self.sio.sid].p=p
        secret_nr=generateExponent(p,False)
        self.sid_dict_client[self.sio.sid].secret_nr=secret_nr
        key=generateExponent(KEY_GENERATING_LIMIT,True)
        print(key)
        self.sid_dict_client[self.sio.sid].key=key
        number=modularExponentation(key,secret_nr,p)
        self.sio.emit('estabilish_secret_start',{'coded_nr': str(number), 'p':str(p)})
        
    def on_server_secret_response(self,data):
        msg=int(data.get('msg'))
        secret_nr=self.sid_dict_client[self.sio.sid].secret_nr
        p=self.sid_dict_client[self.sio.sid].p
        secret_inverse=inverseModular(secret_nr,p)
        response=modularExponentation(msg,secret_inverse,p)
        self.sio.emit('estabilish_secret_end',{'data': str(response)})
        
    def on_secret_recieved_successfully(self):
        record=self.sid_dict_client[self.sio.sid]
        with self.flask_app.app_context():
            createRemote(record.ip_address,record.port,str(record.key))
    
    def on_disconnect_client(self):
        app.logger.info("%s Server severed connection", self.sio.sid)
        
    def find_request_sid(self,ip_address):
        if self.sid_dict_client:
            for key,record in self.sid_dict_client.items():
                if record.ip_address == ip_address:
                    return key
        else:
            return 'Not in database'
        
        
def getSocketServer():
    if not app.socket_server:
        with app.app_context():
            app.socket_server=serverEventsHandler(app.socketio, app)
    return app.socket_server