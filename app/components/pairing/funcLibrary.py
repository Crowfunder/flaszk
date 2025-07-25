from dataclasses import dataclass
from app.database.models import Remote
from app.app import db
import requests
import os
import re

@dataclass
class connectionParameters:
    ip_address: str =None
    stage: int =None
    secret_nr: int=None
    p: int=None
    is_auth: bool=None
    is_paired: bool=None
    port:int=None
    
@dataclass
class connectionParametersClient:
    ip_address: str=None
    secret_nr: int=None
    p: int=None
    key:int=None
    is_auth: bool =None
    is_paired: bool=None
    port:int=None
    
    

def validateIp(ip):
    pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    if not pattern.match(ip):
        return False
    return True

def createRemoteOnClient(address, port, secret):
    local_port=os.getenv('FLASK_RUN_PORT')
    requests.post(f"http://127.0.0.1:{local_port}/remotes/add", json={"address": address, "port": port, "secret": secret})


def createRemote(address,port,secret):
    remote = Remote(
    address=address,
    port=port,
    secret=secret,
    )
    db.session.add(remote)
    db.session.commit()
    
def is_PIN_correct(PIN):
    if PIN == 1234 :
        return True
    return False