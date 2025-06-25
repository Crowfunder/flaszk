from flask import current_app
from sqlalchemy import select

from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from app.database.schema.schemas import DocumentSchema
from app.app import db
from .syncConfig import SERVER_SYNC_ENDPOINT
from ..utils.remoteUtils import checkIfRemoteUp
from ..utils.remoteUtils import remoteSendGetWithSecret
from ..utils.documentUtils import importLocalDocument, importRemoteDocument


def syncWithRemote(remote: Remote):
    response_json = remoteSendGetWithSecret(remote, SERVER_SYNC_ENDPOINT)
    for document in response_json:
        document_hash = document['file_hash']
        importRemoteDocument(document_hash, remote)


def syncWithAll():
    remotes = Remote.query.all()
    for remote in remotes:
        if checkIfRemoteUp(remote):
            try:
                syncWithRemote(remote)
            except:
                continue


def exportLocalDocuments():
    documents = Document.query.filter_by(is_local=True)
    return DocumentSchema(many=True).dump(documents)