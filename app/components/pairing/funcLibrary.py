from dataclasses import dataclass
from app.database.models import Remote
from app.app import db

@dataclass
class connectionParameters:
    ip_address: str
    stage: int
    secret_nr: int
    p: int
    is_auth: bool
    is_paired: bool
    port:int
    
@dataclass
class connectionParametersClient:
    ip_address: str
    secret_nr: int
    p: int
    key:int
    is_auth: bool
    is_paired: bool
    port:int
    
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