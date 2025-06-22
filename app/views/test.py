from flask import Blueprint, request, current_app, g, render_template, flash, redirect, url_for, jsonify
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import datetime


from ..app import db
from ..database.models import *
from ..database.tests import *

bp = Blueprint('bp_test', __name__)

@bp.route('/test', methods=['GET'])
def test():
    db_test(current_app)
    return 200, 'test'