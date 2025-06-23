from flask import current_app
from sqlalchemy import select

from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from app.database.schema.schemas import DocumentSchema
from app.app import db
from ..sync.syncConfig import SERVER_SYNC_ENDPOINT
from ..utils.remoteUtils import checkIfRemoteUp
from ..utils.netUtils import requestGetWithSecret


def importRemoteDocument(document_hash: str, remote: Remote):
    """
    Imports a document from a remote source into the local database.

    Args:
        document_hash (str): The unique hash identifying the document.
        remote (Remote): The Remote object representing the remote source.

    Behavior:
        - If the document does not exist locally, creates a new Document entry with is_local=False.
        - Checks if a DocumentMirror entry exists for the given document_hash and remote.Id.
        - If not, creates a new DocumentMirror entry linking the document to the remote.
        - Commits all changes to the database.
    """
    
    # Check if document has been indexed
    indexedDocument = Document.query.get(document_hash)
    
    # Document was not indexed before
    if not indexedDocument:
        indexedDocument = Document(
            file_hash=document_hash,
            is_local=False
        )
        db.session.add(indexedDocument)
    
    # Check if this mirror already exists
    existingMirror = DocumentMirror.query.filter_by(document_hash=document_hash, remote_Id=remote.Id).one_or_none()
    if not existingMirror:
        mirror = DocumentMirror(
            document_hash=document_hash,
            remote_Id=remote.Id
        )
        db.session.add(mirror)
    db.session.commit()


def importLocalDocument(document_hash: str, file_path: str):
    """
    Imports a local document into the database.

    Args:
        document_hash (str): The unique hash identifying the document.
        file_path (str): The local file path of the document.

    Behavior:
        - Checks if a Document with the given hash already exists.
        - If not, creates a new Document entry with is_local=True and the provided file_path.
        - Commits the new document to the database.
    """
    # Check if document was already indexed
    localDocument = Document.query.get(document_hash)
    
    # Create if not
    if not localDocument:
        localDocument = Document(
            file_hash=document_hash,
            file_path=file_path,
            is_local=True
        )
        db.session.add(localDocument)

    # Document was indexed, but only from remotes
    if not localDocument.is_local():
        localDocument.is_local = True

    db.session.commit()


def syncWithRemote(remote: Remote):
    url = f'{remote.address}:{remote.port}/{SERVER_SYNC_ENDPOINT}'
    response_json = requestGetWithSecret(url, remote.secret)
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