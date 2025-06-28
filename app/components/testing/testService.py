from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from app.app import db
from ..utils.documentUtils import importLocalDocument
from flask import current_app
from sqlalchemy import select

from random import random
from hashlib import sha256


def create_documents():
    # document = Document(
    #     file_hash=sha256(str(random()).encode()).hexdigest(),
    #     file_path='/test/test/abc.txt',
    #     is_local=True,
    # )
    # db.session.add(document)
    # db.session.commit()
    importLocalDocument("C:\\Users\\storm\\OneDrive\\Pulpit\\test.pdf")


def create_remote_5000():
    remote = Remote(
        address="127.0.0.1",
        port=5000,
        secret="supersecret123",
        name="BackgroundNode"
    )
    db.session.add(remote)
    db.session.commit()

def create_remote_5001():
    remote = Remote(
        address="127.0.0.1",
        port=5001,
        secret="supersecret123",
        name="BackgroundNode"
    )
    db.session.add(remote)
    db.session.commit()


def db_test():


    app = current_app
    #####################
    # TODO: remove
    # TESTING
    ###############
    # Create a remote server
    remote = Remote(
        address="127.0.0.1",
        port=5001,
        secret="supersecret123",
        name="BackgroundNode"
    )
    db.session.add(remote)
    db.session.commit()
    # remote1 = Remote(
    #     address="192.168.1.113",
    #     port=8080,
    #     secret="supersecret123",
    #     name="SAMANGo"
    # )
    # db.session.add(remote1)
    # db.session.commit()


    # Create a document
    document = Document(
        file_hash=sha256(str(random()).encode()).hexdigest(),
        file_path="/var/data/doc1.txt",
        is_local=True,
    )
    db.session.add(document)
    db.session.commit()

    # Link the metadata to the document (backref)
    metadata = DocumentMetadata(
        document_hash=document.file_hash  # Will be set after document is created
    )
    db.session.add(metadata)
    db.session.commit()

    # Create a mirror relationship (Document <-> Remote)
    # mirror = DocumentMirror(
    #     document_hash=document.file_hash,
    #     remote_Id=remote.Id
    # )

    # mirror1 = DocumentMirror(
    #     document_hash=document.file_hash,
    #     remote_Id=remote1.Id
    # )
    # db.session.add(mirror)
    # db.session.add(mirror1)
    db.session.commit()

    print("Example entries created!")

    # q    = select(Document).where(Document.file_hash == "abc123def456")
    # r = db.session.scalars(q)
    # for row in r.all():
    #     print(row)
    #     print(row.mirrors)


    # q = select(Remote).where(Remote.Id == 2)
    # r = db.session.scalars(q)
    # for row in r.all():
    #     print(row)
    #     print(row.mirrors)
    #     db.session.delete(row)

    # q = select(DocumentMirror).where(DocumentMirror.Id == 2)
    # r = db.session.scalars(q)
    # for row in r.all():
    #     print(row)
