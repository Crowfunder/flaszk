import datetime
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

# Here you can read about useful column types (Integer, String, DateTime, etc...):
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase-types

# Here you can read about relationships between models:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
# https://stackoverflow.com/questions/3113885/difference-between-one-to-many-many-to-one-and-many-to-many

# Here you can read about using models defined below to work
# with the database (creating rows, selecting rows, deleting rows, etc...):
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/



db = SQLAlchemy()

class DocumentMetadata(db.Model):
    __tablename__ = 'documents_metadata'

    Id = db.Column(db.Integer, primary_key=True)
    document_Id = db.Column(db.Integer, db.ForeignKey('documents.local_Id'), nullable=False)
    document = db.relationship('Document', lazy=True)


class DocumentMirror(db.Model):
    __tablename__ = 'documents_mirrors'

    Id = db.Column(db.Integer, primary_key=True)
    document_Id = db.Column(db.Integer, db.ForeignKey('documents.local_Id'), nullable=False)
    document = db.relationship('Document', lazy=True)
    remote_Id = db.Column(db.Integer, db.ForeignKey('remotes.Id'), nullable=False)
    remote = db.relationship('Remote', lazy=True)
    

class Document(db.Model):
    __tablename__ = 'documents'

    local_Id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String, nullable=True)
    local_file_path = db.Column(db.String, nullable=True)
    is_local = db.Column(db.Boolean, nullable=False, default=False)
    document_metadata_id = db.Column(db.Integer, db.ForeignKey('documents_metadata.Id'), nullable=False)
    document_metadata = db.relationship('DocumentMetadata', backref=db.backref('documents', lazy=True))
    mirrors = db.relationship('DocumentMirror', backref='documents', lazy=True)


class Remote(db.Model):
    __tablename__ = 'remotes'

    Id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    secret = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    mirrors = db.relationship('DocumentMirror', backref='remotes', lazy=True)


