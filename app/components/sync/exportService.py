from flask import current_app
from sqlalchemy import select

from app.database.schema.schemas import DocumentSchema
from app.database.models import Document
from app.app import db

def exportLocalDocuments():
    documents = Document.query.filter_by(is_local=True)
    return DocumentSchema(many=True).dump(documents)