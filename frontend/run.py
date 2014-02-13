#!venv/bin/python
from app import app

import socket
server_ip = str(socket.gethostbyname(socket.gethostname()))
if server_ip == "127.0.1.1" : server_ip = "192.168.199.144"

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    API_SERVER_IP = server_ip,
    API_SERVER_PORT = '5003'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

server_port = 5004
if server_ip == "137.110.160.48": server_port = 80

app.run(host=server_ip, port=server_port)
