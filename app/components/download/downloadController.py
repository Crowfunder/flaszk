from flask import Blueprint

from .downloadConfig import CLIENT_DOWNLOAD_ENDPOINT, SERVER_DOWNLOAD_ENDPOINT, DOWNLOAD_TTL, DOWNLOAD_URL_PARAM
from .downloadService import downloadDocumentFromHash, getRequestFilehash
from ..utils.netUtils import getRequestIP, getRequestSecret
from ..utils.remoteUtils import authenticateRemote

bp = Blueprint('bp_download', __name__)


# Receive file download request on the webpanel
# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_DOWNLOAD_ENDPOINT, methods=['GET'])
def clientDownload():
    file_hash = getRequestFilehash()
    document = downloadDocumentFromHash(file_hash)
    if document:
        return document, 200
    return 'document not found', 404
    

# Receive file download request from other client
@bp.route(SERVER_DOWNLOAD_ENDPOINT, methods=['GET'])
def serverServeDownload():
    remote_ip = getRequestIP()
    secret = getRequestSecret()
    file_hash = getRequestFilehash()
    if authenticateRemote(remote_ip, secret):
        document = downloadDocumentFromHash(file_hash)
        if not document:
            return 'document not found or error', 404
    return 'unknown remote', 403
    