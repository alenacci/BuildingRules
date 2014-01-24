#!venv/bin/python
from app import app

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    HOST_IP="192.168.199.141",
    HOST_PORT=5003
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.run(host="192.168.199.141", port=5003)
