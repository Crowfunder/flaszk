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

    id = db.Column(db.Integer, primary_key=True)
    # Define other metadata fields here as needed


class Document(db.Model):
    __tablename__ = 'documents'

    LocalId = db.Column(db.Integer, primary_key=True)
    FileHash = db.Column(db.String, nullable=True)
    LocalFilePath = db.Column(db.String, nullable=True)
    isLocal = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign key to Metadata
    document_metadata_id = db.Column(db.Integer, db.ForeignKey('documents_metadata.id'), nullable=False)
    document_metadata = db.relationship('DocumentMetadata', backref=db.backref('documents', lazy=True))

    # Relationship to Remote (back-populated)
    remotes = db.relationship('Remote', backref='documents', lazy=True)


class Remote(db.Model):
    __tablename__ = 'remotes'

    Id = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String, nullable=False)
    Port = db.Column(db.Integer, nullable=False)
    Secret = db.Column(db.String, nullable=False)
    Name = db.Column(db.String, nullable=True)

    # Link back to Document
    document_id = db.Column(db.Integer, db.ForeignKey('documents.LocalId'), nullable=False)

