from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime

from app.database.models import Remote, Document, DocumentMetadata, DocumentMirror
from .syncService import syncWithAll, exportLocalDocuments
from .syncConfig import CLIENT_SYNC_ENDPOINT, SERVER_SYNC_ENDPOINT
from ..utils.netUtils import getRequestIP, getRequestSecret
from ..utils.remoteUtils import authenticateRemote
from app.database.schema.schemas import *

bp = Blueprint('bp_sync', __name__)



# Request synchronizing with paired Remotes
# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_SYNC_ENDPOINT, methods=['GET'])
def clientSyncAll():
    syncWithAll()
    flash("Finished syncing", 'info')
    if not request.referrer:
        return 'ok'
    return redirect(request.referrer)


# Receive synchronization request from other remote
@bp.route(SERVER_SYNC_ENDPOINT, methods=['GET'])
def serverSyncAll():
    remote_ip = getRequestIP()
    secret = getRequestSecret()
    if authenticateRemote(remote_ip, secret):
        return exportLocalDocuments(), 200
    return 'unknown remote', 403
    