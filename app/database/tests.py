from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from app.app import db
from flask import current_app
from sqlalchemy import select

def db_test():


    app = current_app
    #####################
    # TODO: remove
    # TESTING
    ###############
    # Create a remote server
    with app.app_context():
        remote = Remote(
            address="192.168.1.100",
            port=8080,
            secret="supersecret123",
            name="BackupNode1"
        )
        db.session.add(remote)
        db.session.commit()
        remote1 = Remote(
            address="192.168.1.113",
            port=8080,
            secret="superseawqwe3",
            name="SAMANGo"
        )
        db.session.add(remote1)
        db.session.commit()


        # Create a document
        document = Document(
            file_hash="abc123def456",
            local_file_path="/var/data/doc1.txt",
            is_local=True,
        )
        db.session.add(document)
        db.session.commit()

        # Link the metadata to the document (backref)
        metadata = DocumentMetadata(
            document_Id=document.local_Id  # Will be set after document is created
        )
        db.session.add(metadata)
        db.session.commit()

        # Create a mirror relationship (Document <-> Remote)
        mirror = DocumentMirror(
            document_Id=document.local_Id,
            remote_Id=remote.Id
        )

        mirror1 = DocumentMirror(
            document_Id=document.local_Id,
            remote_Id=remote1.Id
        )
        db.session.add(mirror)
        db.session.add(mirror1)
        db.session.commit()

        print("Example entries created!")

        q    = select(Document).where(Document.local_Id == 1)
        r = db.session.scalars(q)
        for row in r.all():
            print(row)


        q = select(Remote).where(Remote.Id == 2)
        r = db.session.scalars(q)
        for row in r.all():
            print(row)
            print(row.mirrors)
            db.session.delete(row)

        q = select(DocumentMirror).where(DocumentMirror.Id == 2)
        r = db.session.scalars(q)
        for row in r.all():
            print(row)
