from marshmallow import Schema, fields, EXCLUDE, post_load
from app.database.models import Document, DocumentMetadata, DocumentMirror, Remote


class DocumentMetadataSchema(Schema):
    class Meta:
        model = DocumentMetadata
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    Id = fields.Int(dump_only=True)
    document_hash = fields.Str(required=True)
    file_name = fields.Str(load_default='', allow_none=True)
    title = fields.Str(load_default='', allow_none=True)
    author = fields.Str(load_default='', allow_none=True)
    date = fields.DateTime(allow_none=True)

    @post_load
    def make_metadata(self, data, **kwargs):
        return DocumentMetadata(**data)


class DocumentMirrorSchema(Schema):
    class Meta:
        model = DocumentMirror
        load_instance=True
        include_fk = True

    Id = fields.Int(dump_only=True)
    document_Id = fields.Int(required=True)
    remote_Id = fields.Int(required=True)

class RemoteSchema(Schema):
    class Meta:
        model = Remote
        load_instance=True
        include_fk = True

    Id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    port = fields.Int(required=True)
    secret = fields.Str(required=True)
    # name = fields.Str()
    # mirrors = fields.Nested('DocumentMirrorSchema', many=True, dump_only=True)

class SharedDocumentSchema(Schema):
    '''
    Schema for sharing documents with other Remotes
    '''
    class Meta:
        model = Document
        load_instance=True
        include_fk = True

    # local_Id = fields.Int(dump_only=True)
    file_hash = fields.Str()
    # file_path = fields.Str()
    # is_local = fields.Bool()
    document_metadata = fields.Nested(DocumentMetadataSchema, many=True, dump_only=True)
    # mirrors = fields.Nested(DocumentMirrorSchema, many=True, dump_only=True)

    @post_load
    def make_document(self, data, **kwargs):
        return Document(**data)


class LocalDocumentSchema(Schema):
    '''
    Schema for viewing the documents on local client webpanel
    '''
    class Meta:
        model = Document
        load_instance=True
        include_fk = True

    file_hash = fields.Str()
    file_path = fields.Str()
    is_local = fields.Bool()
    document_metadata = fields.Nested(DocumentMetadataSchema, many=True, dump_only=True)
    mirrors = fields.Nested(DocumentMirrorSchema, many=True, dump_only=True)