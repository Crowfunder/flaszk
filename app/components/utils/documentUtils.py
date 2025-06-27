from ..utils.fileUtils import getFileHash, checkIfFileExists
from app.database.models import Document, Remote, DocumentMetadata, DocumentMirror
from app.app import db

def importLocalDocument(file_path: str):
    """
    Imports a local document into the database.

    Args:
        file_path (str): The local file path of the document.

    Behavior:
        - Checks if a Document with the given hash already exists.
        - If not, creates a new Document entry with is_local=True and the provided file_path.
        - Commits the new document to the database.
    """

    # Calculate document hash
    document_hash = getFileHash(file_path)

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
    if not localDocument.is_local:
        localDocument.is_local = True

    # Perform an integrity check
    # Fix a document with dead file_path
    else: 
        if not checkIfFileExists(localDocument.file_path) or not verifyDocumentHash(localDocument):
            localDocument.file_path = file_path

    db.session.commit()
    return localDocument


def importRemoteDocument(document_hash: str, remote: Remote, document_metadata: DocumentMetadata):
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
            is_local=False,
        )
        db.session.add(indexedDocument)
    
    # Check if metadata of this document is available
    localMetadata = DocumentMetadata.query.filter_by(document_hash=document_metadata.document_hash)

    if not localMetadata:
        db.session.add(document_metadata)


    # Check if this mirror already exists
    existingMirror = DocumentMirror.query.filter_by(document_hash=document_hash, remote_Id=remote.Id).one_or_none()
    if not existingMirror:
        mirror = DocumentMirror(
            document_hash=document_hash,
            remote_Id=remote.Id
        )
        db.session.add(mirror)
    db.session.commit()
    return indexedDocument


def verifyDocumentHash(document: Document):
    return getFileHash(document.file_path) == document.file_hash