from flask import request, send_file
from sqlalchemy import select
import requests

from .downloadConfig import DOWNLOAD_TTL, DOWNLOAD_URL_PARAM, SERVER_DOWNLOAD_ENDPOINT
from app.database.models import Document, DocumentMirror, Remote
from ..utils.fileUtils import checkIfFileExists
from ..utils.documentUtils import verifyDocumentHash
from ..utils.netUtils import getRequestSecret
from ..utils.remoteUtils import remoteSendGetWithSecret
from app.app import db


def getRequestFilehash():
    '''
    Attempt to extract the requested file hash from the request
    Usable only in request context
    '''
    return request.args.get(DOWNLOAD_URL_PARAM)


def getRequestTTL():
    '''
    Attempt to extract the TTL from the download request
    Usable only in request context
    '''
    return request.args.get(str(DOWNLOAD_TTL))


def handleTTL(request_ttl):
    '''
    Decrements the TTL (Time-To-Live) value for a download request.

    Args:
        request_ttl (int): The current TTL value from the request.

    Returns:
        tuple: (bool, int)
            - bool: True if the decremented TTL is still valid (>0), False otherwise.
            - int: The new TTL value after decrement.

    Behavior:
        - Decrements the TTL by 1.
        - If the new TTL is less than 1, returns (False, 0).
        - Otherwise, returns (True, new_ttl).
    '''
    request_ttl = int(request_ttl)  # to assure it's int not str
    request_ttl -= 1
    if request_ttl < 1:
        return False, 0
    return True, request_ttl


def downloadRemoteDocument(document: Document):
    remote_document = None
    mirrors = DocumentMirror.query.filter_by(document_hash=document.file_hash).all()
    for mirror in mirrors:
        try:
            remote = Remote.query.get(mirror.remote_id)
            remote_document = remoteSendGetWithSecret(remote, SERVER_DOWNLOAD_ENDPOINT)
            if remote_document:
                return remote_document
        except:
            continue
    return None


def downloadLocalDocument(document: Document):
    if not checkIfFileExists(document.local_file_path) or not verifyDocumentHash(document):
        return None #  Should also start indexing!!!
    return send_file(document.local_file_path, as_attachment=True)


def downloadDocumentFromHash(file_hash):
    document = Document.query.get(file_hash)
    if not document:
        return None

    if not document.is_local:
        if not document.mirrors:
            return None
        return downloadRemoteDocument(document)
    return downloadLocalDocument(document)


def serveLocalDocument(document: Document):
    if not checkIfFileExists(document.local_file_path) or not verifyDocumentHash(document):
        return None #  Should also start indexing!!!
    return send_file(document.local_file_path, as_attachment=True)


def serveDocumentFromHash(file_hash):
    document = Document.query.get(file_hash)
    if not document:
        return None
    
    if document.is_local:
        return serveLocalDocument(document)
    
    return None
    
    # serveRemoteDocument(), for public networks only, not for now though