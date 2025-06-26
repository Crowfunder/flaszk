from flask import request

from .clientConfig import DOCUMENT_URL_PARAM
from app.database.models import DocumentMetadata, Document, DocumentMirror
from app.app import db

def getRequestFilehash():
    '''
    Attempt to extract the requested file hash from the request
    Usable only in request context
    '''
    return request.args.get(DOCUMENT_URL_PARAM)