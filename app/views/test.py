from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify, Response
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime


from ..app import db
from ..database.models import *
from ..database.tests import *

bp = Blueprint('bp_test', __name__)

@bp.route('/test/dbinit', methods=['GET'])
def dbinit():
    db_test()
    return 200

@bp.route('/test/dumpdb', methods=['GET'])
def dumpdb():
    r = dump_documents()
    return r, 200