import os
import os.path
import datetime

from .indexConfig import INDEXED_EXTS, INDEXED_PATHS
from app.database.models import DocumentMetadata, Document, DocumentMirror
from app.app import db
from ..utils.documentUtils import importLocalDocument
from ..utils.fileUtils import checkIfFileExists


def initalizeParserDict():
    from .parsers.parser_docx import DocxParser
    from .parsers.parser_pdf import PdfParser
    from .parsers.parser_epub import EpubParser

    docx = DocxParser()
    pdf = PdfParser()
    epub = EpubParser()

    parsers = {}
    parsers[docx.get_ext()] = docx
    parsers[pdf.get_ext()] = pdf
    parsers[epub.get_ext()] = epub

    return parsers


def getFileModDate(file_path: str):
    mtime = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(mtime)


def getFileName(file_path: str):
    if '/' in file_path:
        filename = file_path.split('/')[-1]
    elif '\\' in file_path:
        filename = file_path.split('\\')[-1]
    else:
        filename = file_path

    return filename


def getFileExtension(file_path: str):
    return file_path.split('.')[-1]


def parseDocumentMetadata(document: Document, parsers: dict):
    # Check if metadata for this file exists
    metadata = DocumentMetadata.query.filter_by(document_hash=document.file_hash).first()
    if not metadata:
        metadata = DocumentMetadata(document_hash = document.file_hash)
        db.session.add(metadata)

    file_path = document.file_path

    # Get local filename
    metadata.file_name = getFileName(file_path)

    # Get file modification timestamp
    metadata.date = getFileModDate(file_path)

    # Parse format-specific metadata
    file_ext = getFileExtension(file_path)
    if file_ext:
        try:
            parser = parsers[file_ext]
            metadata_parsed = parser(file_path)
            metadata.title = metadata_parsed.title
            metadata.author = metadata_parsed.author
        except KeyError:
            pass

    db.session.commit()

    
def list_all_files(directory_path: str):
    """
    Returns a list of all files (with full paths) in the given directory and its subdirectories.

    Args:
        directory (str): The root directory to search.

    Returns:
        list[str]: List of full file paths.
    """
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for name in files:
            file_paths.append(os.path.join(root, name))
    return file_paths


def startIndexing():

    parsers = initalizeParserDict()
    for directory_path in INDEXED_PATHS:
        for file_path in list_all_files(directory_path):
            file_ext = getFileExtension(file_path)
            if file_ext in INDEXED_EXTS:
                document = importLocalDocument(file_path)
                parseDocumentMetadata(document, parsers)
    # We probably want to invoke pruning after indexing
    pruneIndex()

    
def pruneIndex():

    documents = Document.query.filter_by(is_local=True).all()
    for document in documents:
        if not checkIfFileExists(document.file_path):
            # Check if document has any mirrors, delete it if not
            if not DocumentMirror.query.filter_by(document_hash=document.file_hash).all():
                db.session.delete(document)
            else:
                document.is_local = False
    db.session.commit()
            