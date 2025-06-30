from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response

from app.database.models import Document, DocumentMetadata, DocumentMirror, Remote
from app.database.schema.schemas import LocalDocumentSchema, DocumentMirrorSchema
from .clientConfig import CLIENT_METADATA_ENDPOINT, CLIENT_DOCUMENT_ENDPOINT, CLIENT_MIRRORS_ENDPOINT
from .clientService import getRequestFilehash

bp = Blueprint('bp_client', __name__)



# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_DOCUMENT_ENDPOINT, methods=['GET'])
def clientGetDocument():
    file_hash = getRequestFilehash()
    documents = Document.query.get(file_hash)
    return LocalDocumentSchema(many=False).dump(documents)


# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_MIRRORS_ENDPOINT, methods=['GET'])
def clientGetDocumentMirrors():
    file_hash = getRequestFilehash()
    mirrors = DocumentMirror.query.filter_by(document_hash=file_hash).all()
    return DocumentMirrorSchema(many=True).dump(mirrors)


# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_METADATA_ENDPOINT, methods=['GET'])
def clientGetDocumentMetadata():
    file_hash = getRequestFilehash()
    metadata = DocumentMetadata.query.filter_by(document_hash=file_hash).first()
    return DocumentMirrorSchema(many=False).dump(metadata)