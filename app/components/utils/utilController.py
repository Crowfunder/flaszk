from flask import Blueprint

from app.database.schema.schemas import *
from .netConfig import SERVER_PING_BUSY, SERVER_PING_ENDPOINT, SERVER_PING_OK

bp = Blueprint('bp_util', __name__)


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