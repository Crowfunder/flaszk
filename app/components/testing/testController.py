from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime
from time import sleep


from app.app import db, pin
from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from .testService import db_test, create_remote_5000, create_remote_5001, create_documents
from app.database.schema.schemas import *
import os
from ..pairing.serverEvents import getSocketServer

bp = Blueprint('bp_test', __name__)


@bp.route('/test/strtserver')
def strtserver():
    port=os.getenv('FLASK_RUN_PORT')
    getSocketServer().run('0.0.0.0',port)
    return 'ok'

@bp.route('/test/strtserver/pair5001')
def pair5001():
    getSocketServer().initilaizeConnection('127.0.0.1',5001)
    return 'ok'

@bp.route('/test/dbinit', methods=['GET'])
def dbinit():
    db_test()
    return "oke"

@bp.route('/test/dumpdb', methods=['GET'])
def dumpdb():
    r = Document.query.all()
    r = SharedDocumentSchema(many=True).dump(r)
    return r, 200


@bp.route('/test/remote5000', methods=['GET'])
def remote5000():
    create_remote_5000()
    return "oke"

@bp.route('/test/remote5001', methods=['GET'])
def remote50001():
    create_remote_5001()
    return "oke"


@bp.route('/test/createdoc', methods=['GET'])
def createdoc():
    create_documents()
    return "oke"

@bp.route('/test/remotes', methods=['GET'])
def allremotes():
    r = Remote.query.all()
    r = RemoteSchema(many=True).dump(r)
    return r, 200

@bp.route('/test/pin', methods=['GET'])
def getpin():
    return pin.get_pin(), 200
