from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response, session
from app.settings.settingsManager import settingsManager

from app.database.models import Document, DocumentMetadata, DocumentMirror, Remote
from app.database.schema.schemas import LocalDocumentSchema, DocumentMirrorSchema
from .clientConfig import CLIENT_METADATA_ENDPOINT, CLIENT_DOCUMENT_ENDPOINT, CLIENT_MIRRORS_ENDPOINT
from .clientService import getRequestFilehash
from app.components.pairing.pin.pinManager import pin

bp = Blueprint('bp_client', __name__)


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
    connection_logs = []

    if request.method == 'POST':
        # Handle settings update for both simple and list fields
        form_data = request.form.to_dict(flat=False)
        settingsManager.update_from_dict(form_data)
        return redirect(url_for('bp_client.settings'))

    pairing_info = session.get('pairing_info')
    return render_template(
        'settings.html',
        settings_dict=settingsManager.as_nested_dict(),
        connection_logs=connection_logs,
        pairing_info=pairing_info,
    )

@bp.route('/settings/restore', methods=['POST'])
def restore_settings():
    settingsManager.restore_defaults()
    return redirect(url_for('bp_settings.settings'))


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