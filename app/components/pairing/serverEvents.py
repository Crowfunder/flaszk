from flask import request, Blueprint
from flask import current_app as app
from flask_socketio import *
from .funcLibrary import *
from .modularEquations import *
import os
import socketio

bp = Blueprint('bp_server', __name__)

class serverEventsHandler():
    def __init__(self,socketIO):
        self.socketio= socketIO
        self.sio=socketio.Client()
        self.sid_dict_server={}
        self.sid_dict_client={}
        self.register_handlers_pairing_server()
        self.register_handlers_pairing_client()
    
    def run(self,server_ip,server_port):
        self.server_ip=server_ip
        self.server_port=server_port
        self.socketio.run(app,f'host={self.server_ip}',f'port={self.server_port}') #odpalenie nasłuchiwania serwera na danym ip i porcie
            
    def register_handlers_pairing_server(self):
        self.socketio.on_event('connect', self.on_connect)
        self.socketio.on_event('verificate_PIN', self.on_verificate_PIN)
        self.socketio.on_event('estabilish_secret_start', self.on_estabilish_secret_start)
        self.socketio.on_event('estabilish_secret_end', self.on_estabilish_seceret_end)
        self.socketio.on_event('disconnect', self.on_disconnect)
        
    def on_connect(self):
        app.logger.info("%s Server connected with new client",request.sid)
        self.socketio.emit('server_welcome',to=request.sid)
        
    def on_verificate_PIN(self,data):
        ip_address=data.get('ip_address')
        port=data.get('port')
        PIN=data.get('pin')
        if is_PIN_correct(PIN):
            self.socketio.emit('is_PIN_correct',{'msg': 'Right PIN given'},to=request.sid)
            self.sid_dict_server[request.sid]=connectionParameters(stage=1, ip_address=ip_address,port=port,is_paired=False)
            app.logger.info("%s Server PIN successfully verified",request.sid)  
        else:
            app.logger.info("%sPIN veirfication unsuccessfull",request.sid)
            self.socketio.send('disconect_client', to=request.sid)
            self.socketio.disconnect(request.sid)
                
    def on_estabilish_secret_start(self,data):
        if self.sid_dict_server[request.sid].stage == 1:
            coded_nr=int(data.get('coded_nr'))
            self.sid_dict_server[request.sid].p=int(data.get('p'))
            p=self.sid_dict_server[request.sid].p
            generated_nr=generateExponent(p)
            self.sid_dict_server[request.sid].secret_nr=generated_nr
            
            msg=modularExponentation(coded_nr,generated_nr,p)
            self.socketio.emit('server_secret_resonse',{'msg': msg},to=request.sid)
            
            self.sid_dict_server[request.sid].stage=2
            app.logger.info("%sFirst Shamir response succesfull",request.sid)
        else:
            app.logger.info("%sFirst Shamir response unsuccesfull",request.sid)
            self.socketio.send('disconect_client', to=request.sid)
            self.socketio.disconnect(request.sid)
            del self.sid_dict_server[request.sid]
            

    def on_estabilish_seceret_end(self,data):
        if self.sid_dict_server[request.sid]==2:
            coded_nr=int(data.get('coded_nr'))
            secret_nr=self.sid_dict_server[request.sid].secret_nr
            p=self.sid_dict_server[request.sid].p
            secret=modularExponentation(coded_nr,(-1)*secret_nr,p)
            
            record=self.sid_dict_server[request.sid]
            createRemote(record.ip_address,record.port,record.se)
            
            self.socketio.send('secret_recieved_successfully',to=request.sid)
            self.sid_dict_server[request.sid].is_paired=True
        else:
            self.socketio.send('disconect_client', to=request.sid)
            self.socketio.disconnect(request.sid)
            del self.sid_dict_server[request.sid]
        
    def on_disconnect(self):
        app.logger.info("%s Server disconnected", request.sid)
        del self.sid_dict_server[request.sid]
        
    def register_handlers_pairing_client(self):
        self.sio.on('server_welcome', self.on_server_welcome)
        self.sio.on('is_PIN_correct', self.on_is_PIN_correct)
        self.sio.on('server_secret_response',self.on_server_secret_response)
        self.sio.on('disconnect_client', self.on_disconnect_client)
        self.sio.on('secret_recieved_successfully',self.on_secret_recieved_successfully)
    
    def initilaizeConnection(self,server_ip_address,port):
        self.server_ip=server_ip_address
        self.port=port
        self.sio.connect(f'http://{server_ip_address}:{port}') # defined port --> to be decided later
        
    # def initilaizeConnection(self,server_ip_address):
    #     self.server_ip=server_ip_address
    #     self.port=80
    #     self.sio.connect(f'http://{server_ip_address}')  #in this case default port is 80 (http comunication)

    def on_server_welcome(self):
        self.sid_dict_client[self.sio.sid]=connectionParametersClient(ip_address=self.server_ip,port=self.port)
        self.sio.emit('verificate_PIN',{'ip_address':self.ip,'pin' : 1234},to=self.sio.sid)
        
    def on_is_PIN_correct(self,data):
        msg=data.get('msg')
        p=generateExponent(5000)
        self.sid_dict_client[self.sio.sid].p=p
        secret_nr=generateExponent(p)
        self.sid_dict_client[self.sio.sid].secret_nr=secret_nr
        key=generateExponent(5000)
        self.sid_dict_client[self.sio.sid].key=key
        number=modularExponentation(key,secret_nr,p)
        self.sio.emit('on_estbilish_secret_start',{'coded_nr': number, 'p':p})
        
    def on_server_secret_response(self,data):
        msg=int(data.get('msg'))
        secret_nr=self.sid_dict_client[self.sio.sid].secret_nr
        p=self.sid_dict_client[self.sio.sid].p
        response=modularExponentation(msg,(-1)*secret_nr,p)
        self.sio.emit('estabilish_secret_end',{'data': response},to=self.sio.sid)
        
    def on_secret_recieved_successfully(self):
        record=self.sid_dict_client[request.id]
        createRemote(record.ip_address,record.port,record.key)
    
    def on_disconnect_client():
        app.logger.info("%s Server severed connection", self.sio.sid)
        
    def find_request_sid(self,ip_address):
        if self.sid_dict_client:
            for key,record in self.sid_dict_client.items():
                if record.ip_address == ip_address:
                    return key
        else:
            return 'Not in database'
        