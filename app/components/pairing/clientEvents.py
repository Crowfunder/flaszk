from flask import request
from flask_socketio import emit, disconnect


class clientEvents():
    def __init__(self,client_ip,socketio):
        self.sio=socketio.Client() 
        self.sid=None
        self.ip=client_ip
        
    def initilaizeConnection(self,server_ip_address,port):
        self.sio.connect(f'http://{server_ip_address}:{port}') # defined port --> to be decided later
        
    def initilaizeConnection(self,server_ip_address):
        self.sio.connect(f'http://{server_ip_address}')  #in this case default port is 80 (http comunication)

