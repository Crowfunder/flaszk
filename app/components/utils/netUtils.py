from flask import request, jsonify
import requests

from .netConfig import SERVER_PING_BUSY, SERVER_PING_ENDPOINT, SECRET_HEADER, HOST_TIMEOUT

def getRequestIP():
    '''
    Try to get real IP if behind a proxy. 
    Usable only in request context
    '''
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip


def getRequestSecret():
    return request.headers.get(SECRET_HEADER)


def checkIfHostUp(ip_addr, port):
    '''
    Utility for checking if the host under specified ip and port is up and available
    '''
    try:
        response = requests.get(f'http://{ip_addr}:{port}/{SERVER_PING_ENDPOINT}', timeout=HOST_TIMEOUT)
        if response.status_code == SERVER_PING_BUSY:
            return False
        return True
    except requests.exceptions.RequestException as e:
        return False
    

def requestGetWithSecret(url, secret):
    headers = {
        SECRET_HEADER : secret
    }
    if 'http' not in url:
        url = 'http://' + url
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
