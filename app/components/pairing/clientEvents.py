from flask import request, app
from flask_socketio import *
from modularEquations import *
from funcLibrary import connectionParametersClient,createRemote
import socketio


class clientEvents():
    def __init__(self,client_ip):
        self.socketio=socketio.Client
        self.ip=client_ip
        self.server_ip=None
        self.sid_dictionary={}
        
    def register_handlers_pairing_client(self):
        self.socketio.on_event('server_welcome', self.on_server_welcome)
        self.socketio.on_event('is_PIN_correct', self.on_is_PIN_correct)
        self.socketio.on_event('server_secret_response',self.on_server_secret_response)
        self.socketio.on_event('disconnect_client', self.on_disconnect_client)
        self.socketio.on_event('secret_recieved_successfully',self.on_secret_recieved_successfully)
    
    def initilaizeConnection(self,server_ip_address,port):
        self.server_ip=server_ip_address
        self.port=port
        self.socketio.connect(f'http://{server_ip_address}:{port}') # defined port --> to be decided later
        
    def initilaizeConnection(self,server_ip_address):
        self.server_ip=server_ip_address
        self.port=80
        self.socketio.connect(f'http://{server_ip_address}')  #in this case default port is 80 (http comunication)

    def on_server_welcome(self):
        self.sid_dictionary[request.sid]=connectionParametersClient(ip_address=self.server_ip,port=self.port)
        self.socketio.emit('verificate_PIN',{'ip_address':self.ip},to=request.sid)
        
    def on_is_PIN_correct(self,data):
        msg=data.get('msg')
        p=generateExponent(5000)
        self.sid_dictionary[request.sid].p=p
        secret_nr=generateExponent(p)
        self.sid_dictionary[request.sid].secret_nr=secret_nr
        key=generateExponent(5000)
        self.sid_dictionary[request.sid].key=key
        number=modularExponentation(key,secret_nr,p)
        self.socketio.emit('on_estbilish_secret_start',{'coded_nr': number, 'p':p})
        
    def on_server_secret_response(self,data):
        msg=int(data.get('msg'))
        secret_nr=self.sid_dictionary[request.sid].secret_nr
        p=self.sid_dictionary[request.sid].p
        response=modularExponentation(msg,(-1)*secret_nr,p)
        self.socketio.emit('estabilish_secret_end',{'data': response},to=request.sid)
        
    def on_secret_recieved_successfully(self):
        record=self.sid_dictionary[request.id]
        createRemote(record.ip_address,record.port,record.key)
        pass
    
    def on_disconnect_client():
        app.logger.info("%s Server severed connection", request.sid)