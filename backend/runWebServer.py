#!venv/bin/python
from app import app

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

import socket
server_ip = str(socket.gethostbyname(socket.gethostname()))
if server_ip == "127.0.1.1" : server_ip = "192.168.199.144"

app.run(host=server_ip, port=5003)
