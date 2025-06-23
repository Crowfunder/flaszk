from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime

from app.app import db
from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from .importService import syncWithAll
from .exportService import exportLocalDocuments, authenticateRequestor
from .utils.netutils import getRequestIP
from app.database.schema.schemas import *

bp = Blueprint('bp_util', __name__)

SERVER_PING_ENDPOINT = '/server/ping'
SERVER_PING_BUSY = 503
SERVER_PING_OK = 200


# Endpoint for getting pinged for hosts to get the following information
# - Is the server reachable for the requester?
# - Is the server ready to take a sync request? (Not busy with indexing)'
# TODO: Should be implemented by checking a global flag that gets raised
#       when indexing is ongoing.
@bp.route(SERVER_PING_ENDPOINT, methods=['GET'])
def isServerBusy():
    busy = 0
    if busy:
        return 'server busy', SERVER_PING_BUSY
    return 'server ready', SERVER_PING_OK