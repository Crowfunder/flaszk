from flask import request,app
from flask_socketio import emit, disconnect


class serverEventsHandler():
    def __init__(self,socketio,ip_address,port):
        self.socketio=socketio
        self.ip=ip_address
        self.b_secret=None
        self.socketio.run(app,f'host={ip_address}',f'port={port}') #odpalenie nasłuchiwania serwera na danym ip i porcie
        
    

    def register_events(self):    
        @self.socketio.on("connect")
        def on_connect():
            self.socketio.emit('server_welcome',to=request.sid)
            app.logger.info("%s Server sent server_welcome message", request.sid)
            # Dodawanie do bazy danych
            
        @self.socketio.on("estabilish_secret_start")
        def on_estabilish_seceret_start(data,p):
            if self.b_secret == None:
                self.b_secret=generateExponent()
                msg=modularExponentiation(data,self.b_secret,p)
                self.socketio.emit('server_secret_resonse',msg)
            else:
                self.socketio.emit('Other_device_is_pairing')
            
        @self.socketio.on("estabilish_seceret_end")
        def on_estabilish_seceret_end(data,p):
            secret=modularInverse(data,self.b_secret,p)
            #zapisanie sekretu do bazy danych
            self.b_secret=None
            
        @self.socketio.on('disconnect')
        def on_disconnect():
            app.logger.info("%s Server disconnected", request.sid)
            # usuwanie z bazy danych
        
        
