from flask import current_app
from sqlalchemy import select
from marshmallow import ValidationError

from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from app.database.schema.schemas import SharedDocumentSchema, DocumentMetadataSchema
from app.app import db
from .syncConfig import SERVER_SYNC_ENDPOINT
from ..utils.remoteUtils import checkIfRemoteUp
from ..utils.remoteUtils import remoteSendGetWithSecret
from ..utils.documentUtils import importLocalDocument, importRemoteDocument


def syncWithRemote(remote: Remote):
    """
    Synchronizes documents from a remote server.

    Args:
        remote (Remote): The Remote object representing the remote server.

    Behavior:
        - Sends a GET request to the remote's SERVER_SYNC_ENDPOINT.
        - Iterates over the returned documents.
        - For each document, calls importRemoteDocument to import it locally.
    """
    response_json = remoteSendGetWithSecret(remote, SERVER_SYNC_ENDPOINT).json()
    for document in response_json:
        document_hash = document['file_hash']
        document_metadata_json = document['document_metadata']
        try:
            document_metadata = DocumentMetadataSchema().load(document_metadata_json)
        except ValidationError as err:
            document_metadata = DocumentMetadata(document_hash=document_hash)
        importRemoteDocument(document_hash, remote, document_metadata)


def syncWithAll():
    """
    Synchronizes documents from all available remotes that are up.

    Behavior:
        - Queries all Remote entries.
        - For each remote, checks if it is up using checkIfRemoteUp.
        - If up, calls syncWithRemote to synchronize documents.
        - Ignores remotes that are down or cause exceptions.
    """
    remotes = Remote.query.all()
    for remote in remotes:
        if checkIfRemoteUp(remote):
            try:
                syncWithRemote(remote)
            except:
                continue


def exportLocalDocuments():
    """
    Exports all local documents as a list of serialized dictionaries.

    Returns:
        list: A list of serialized local Document objects using DocumentSchema.
    """
    documents = Document.query.filter_by(is_local=True)
    return SharedDocumentSchema(many=True).dump(documents)