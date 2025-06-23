from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime


from app.app import db
from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from .testService import db_test
from app.database.schema.schemas import *

bp = Blueprint('bp_test', __name__)



@bp.route('/test/dbinit', methods=['GET'])
def dbinit():
    db_test()
    return "oke"

@bp.route('/test/dumpdb', methods=['GET'])
def dumpdb():
    r = Document.query.all()
    r = DocumentSchema(many=True).dump(r)
    return r, 200

