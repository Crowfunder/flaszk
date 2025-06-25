from flask import request, send_file, Response
from sqlalchemy import select
from hashlib import sha256

from .downloadConfig import DOWNLOAD_TTL, DOWNLOAD_URL_PARAM, SERVER_DOWNLOAD_ENDPOINT
from app.database.models import Document, DocumentMirror, Remote
from ..utils.fileUtils import checkIfFileExists
from ..utils.documentUtils import verifyDocumentHash
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
    return request.headers.get(str(DOWNLOAD_TTL))


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
    mirrors = DocumentMirror.query.filter_by(document_hash=document.file_hash).all()
    for mirror in mirrors:
        try:
            remote = Remote.query.get(mirror.remote_Id)
            file_param = f'?{DOWNLOAD_URL_PARAM}={document.file_hash}'
            resp = remoteSendGetWithSecret(remote, SERVER_DOWNLOAD_ENDPOINT+file_param)

            # Verify checksum!
            if resp and document.file_hash == sha256(resp.content).hexdigest():
                # Build flask-compatible response
                flask_response = Response(
                    response=resp.content,
                    status=resp.status_code,
                    content_type=resp.headers.get('Content-Type')
                )
                return flask_response
        except Exception as e:
            continue
    return None


def downloadLocalDocument(document: Document):
    """
    Serves a local document as a file download if it exists.

    Args:
        document (Document): The Document object to serve.

    Returns:
        Response: Flask response with the file as an attachment, or None if not found or invalid.
    """
    if not checkIfFileExists(document.file_path) and verifyDocumentHash(document):
        return None  # Should also start indexing!
    return send_file(document.file_path, as_attachment=True)


def downloadDocumentFromHash(file_hash):
    """
    Downloads a document by its file hash, serving it locally or fetching from a remote mirror.

    Args:
        file_hash (str): The hash of the document to download.

    Returns:
        Response: Flask response with the file, or None if not found.
    """
    document = Document.query.get(file_hash)
    if not document:
        return None

    if not document.is_local:
        if not document.mirrors:
            return None
        response = downloadRemoteDocument(document)
    else:
        response = downloadLocalDocument(document)

    return response


def serveDocumentFromHash(file_hash):
    """
    Serves a document by its file hash if it is local.

    Args:
        file_hash (str): The hash of the document to serve.

    Returns:
        Response: Flask response with the file, or None if not found or not local.
    """
    document = Document.query.get(file_hash)
    if not document:
        return None

    if document.is_local:
        return downloadLocalDocument(document)

    return