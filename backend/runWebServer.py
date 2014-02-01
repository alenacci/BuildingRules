#!venv/bin/python
from app import app

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.run(host="192.168.199.141", port=5003)
