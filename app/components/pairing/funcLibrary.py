from dataclasses import dataclass
from app.database.models import Remote
from app.app import db

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