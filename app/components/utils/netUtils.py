from flask import request, jsonify
import requests

from .netConfig import SERVER_PING_BUSY, SERVER_PING_ENDPOINT, SECRET_HEADER, HOST_TIMEOUT, REQUEST_PROTOCOL

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
    '''
    Attempt to extract the header containing the secret.
    Usable only in request context
    '''
    return request.headers.get(SECRET_HEADER)


def checkIfHostUp(ip_addr, port):
    '''
    Utility for checking if the host under specified IP and port is up and available.

    Args:
        ip_addr (str): The IP address of the host to check.
        port (int or str): The port number to check on the host.

    Returns:
        bool: True if the host is up and not busy, False otherwise.

    Behavior:
        - Sends a GET request to 'http://{ip_addr}:{port}/{SERVER_PING_ENDPOINT}' with a timeout of HOST_TIMEOUT.
        - If the response status code is SERVER_PING_BUSY, returns False.
        - If the request is successful and the host is not busy, returns True.
        - If any exception occurs (e.g., timeout, connection error), returns False.
    '''
    try:
        response = requests.get(f'{REQUEST_PROTOCOL}://{ip_addr}:{port}/{SERVER_PING_ENDPOINT}', timeout=HOST_TIMEOUT)
        if response.status_code == SERVER_PING_BUSY:
            return False
        return True
    except requests.exceptions.RequestException as e:
        return False
    

def requestGetWithSecret(url, secret, extra_headers={}):
    '''
    Sends a GET request to the specified URL with a secret included in the headers.

    Args:
        url (str): The URL to send the GET request to. If the URL does not start with 'http', {REQUEST_PROTOCOL}:// is prepended.
        secret (str): The secret value to include in the request headers.

    Returns:
        dict: The JSON response from the server.

    Raises:
        requests.HTTPError: If the response contains an HTTP error status code.

    Behavior:
        - Adds the secret to the request headers using the SECRET_HEADER key.
        - Sends a GET request to the given URL.
        - Raises an exception if the request fails.
        - Returns the parsed JSON response.
    '''
    headers = {
        SECRET_HEADER : secret
    }
    headers.update(extra_headers)
    if REQUEST_PROTOCOL not in url:
        url = f'{REQUEST_PROTOCOL}://' + url
    response = requests.get(url, headers=headers, timeout=HOST_TIMEOUT)
    response.raise_for_status()
    return response.json()
