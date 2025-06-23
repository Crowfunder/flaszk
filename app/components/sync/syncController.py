from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime

from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from .importService import syncWithAll
from .exportService import exportLocalDocuments
from ..utils.netUtils import getRequestIP
from ..utils.remoteUtils import authenticateRemote
from app.database.schema.schemas import *

bp = Blueprint('bp_sync', __name__)

SERVER_SYNC_ENDPOINT = '/server/sync/all'

# Request synchronizing with paired Remotes
@bp.route('/client/sync/all', methods=['GET'])
def clientSyncAll():
    syncWithAll()
    return 'synced', 200


# Receive synchronization request from other remote
@bp.route(SERVER_SYNC_ENDPOINT, methods=['GET'])
def serverSyncAll():
    remote_ip = getRequestIP()
    secret = 'supersecret123'
    if authenticateRemote(remote_ip, secret):
        return exportLocalDocuments(), 200
    
    