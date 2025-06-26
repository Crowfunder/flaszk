from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime

from indexerConfig import CLIENT_INDEX_ENDPOINT
from indexerService import startIndexing

bp = Blueprint('bp_index', __name__)



# Start indexing local documents
# TODO: Secure with @login_required !!!!
@bp.route(CLIENT_INDEX_ENDPOINT, methods=['GET'])
def clientIndexing():
    startIndexing()
    return 'indexed', 200