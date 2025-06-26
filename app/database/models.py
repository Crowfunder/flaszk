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
from dataclasses import dataclass

@dataclass
class DocumentMetadata(db.Model):
    __tablename__ = 'documents_metadata'

    Id = db.Column(db.Integer, primary_key=True)
    document_hash = db.Column(db.String, db.ForeignKey('documents.file_hash', ondelete='CASCADE'), nullable=False)
    file_name = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, nullable=True)


@dataclass
class Document(db.Model):
    __tablename__ = 'documents'

    file_hash = db.Column(db.String, primary_key=True, nullable=False)
    file_path = db.Column(db.String, nullable=True)
    is_local = db.Column(db.Boolean, nullable=False, default=False)
    document_metadata = db.relationship('DocumentMetadata', cascade='all, delete', backref=db.backref('documents', lazy=True))
    mirrors = db.relationship('DocumentMirror', cascade='all, delete', backref='documents', lazy=True)

@dataclass
class DocumentMirror(db.Model):
    __tablename__ = 'documents_mirrors'

    Id = db.Column(db.Integer, primary_key=True)
    document_hash = db.Column(db.String, db.ForeignKey('documents.file_hash', ondelete='CASCADE'), nullable=False)
    remote_Id = db.Column(db.Integer, db.ForeignKey('remotes.Id', ondelete='CASCADE'), nullable=False)

@dataclass
class Remote(db.Model):
    __tablename__ = 'remotes'

    Id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    secret = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    mirrors = db.relationship('DocumentMirror', cascade='all, delete', backref='remotes', lazy=True)


