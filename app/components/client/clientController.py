from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response

from app.database.models import Document, DocumentMetadata, DocumentMirror, Remote
from app.database.schema.schemas import LocalDocumentSchema, DocumentMirrorSchema
from .clientConfig import CLIENT_METADATA_ENDPOINT, CLIENT_DOCUMENT_ENDPOINT, CLIENT_MIRRORS_ENDPOINT
from .clientService import getRequestFilehash
from app.components.pairing.pin.pinManager import pin

bp = Blueprint('bp_client', __name__)

# Example additions to app.py or a blueprint

@bp.route('/')
def home():
    # Fetch all local documents with metadata
    documents = Document.query.all()
    return render_template('index.html', documents=documents)

@bp.route('/document/<file_hash>')
def document_detail(file_hash):
    document = Document.query.get(file_hash)
    return render_template('document_detail.html', document=document)

@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    # Handle pairing form and logs
    my_ip = '127.0.0.1'  # Replace with actual logic
    my_port = 5000       # Replace with actual logic
    my_pin = pin.get_pin()  # Use your pin manager
    connection_logs = []    # Replace with actual logs
    if request.method == 'POST':
        # Handle pairing logic
        ...
    return render_template('settings.html', my_ip=my_ip, my_port=my_port, my_pin=my_pin, connection_logs=connection_logs)

@bp.route('/sync', methods=['POST'])
def sync():
    # Call your sync logic
    ...
    return redirect(url_for('home'))

@bp.route('/index_docs', methods=['POST'])
def index_docs():
    # Call your indexing logic
    ...
    return redirect(url_for('home'))

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