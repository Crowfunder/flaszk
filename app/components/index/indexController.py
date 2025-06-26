from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime

from .indexConfig import CLIENT_INDEX_ENDPOINT, CLIENT_PRUNE_ENDPOINT
from .indexService import startIndexing, pruneIndex

bp = Blueprint('bp_index', __name__)



# Start indexing local documents
# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_INDEX_ENDPOINT, methods=['GET'])
def clientIndexing():
    startIndexing()
    return 'indexed', 200

@bp.route(CLIENT_PRUNE_ENDPOINT, methods=['GET'])
def clientPrune():
    pruneIndex()
    return 'pruned', 200