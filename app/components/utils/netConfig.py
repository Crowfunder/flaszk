# Server Ping Config
SERVER_PING_ENDPOINT = '/server/ping'
SERVER_PING_BUSY = 503
SERVER_PING_OK = 200

# General connectivity settings
HOST_TIMEOUT = 5  # seconds, timeout after which a host is considered unreachable
REQUEST_PROTOCOL = 'http'  # protocol to use when invoking HTTP requests, may be http or https

# Secret passing in request configuration
SECRET_HEADER = 'Remote-Secret'
