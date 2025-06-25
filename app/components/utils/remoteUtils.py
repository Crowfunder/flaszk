from flask import request

from app.database.models import Remote, Document
from .netUtils import checkIfHostUp, requestGetWithSecret


def authenticateRemote(ip_address, secret):
    """
    Authenticates a remote requestor based on their IP address and provided secret.

    Args:
        ip_address (str): The IP address of the requestor.
        secret (str): The secret key provided by the requestor.

    Returns:
        bool: True if authentication is successful, False otherwise.

    Behavior:
        - Looks up a Remote entry matching the given IP address.
        - If no such Remote exists, returns False.
        - If the provided secret does not match the Remote's secret, returns False.
        - Returns True if both checks pass.
    """

    # Assure that the remote IP is known
    remote = Remote.query.filter_by(address=ip_address).one_or_none()
    # remote = Remote.query.filter_by(address=ip_address).all()[0] THIS MAY BE USEFUL FOR LOCAL DOUBLE SERVER TESTING!!
    if not remote:
        return False

    # Check if the secret is correct
    if remote.secret != secret:
        return False
    return True


def checkIfRemoteUp(remote: Remote):
    '''
    Wrapper for `netutils.checkIfHostUp()` that processes Remote objects.
    '''
    return checkIfHostUp(remote.address, remote.port)


def remoteSendGetWithSecret(remote: Remote, endpoint, extra_headers = {}):
    '''
    Wrapper for `netUtils.requestGetWithSecret()` that processes Remote objects.
    '''
    url = f'{remote.address}:{remote.port}/{endpoint}'
    return requestGetWithSecret(url, remote.secret, extra_headers)