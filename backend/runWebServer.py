#!venv/bin/python
from app import app

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import socket
server_ip = str(socket.gethostbyname(socket.gethostname()))

app.run(host=server_ip, port=5003)
