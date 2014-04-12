#!flask/bin/python
from app import app

app.run(debug = True,port=2001,host="0.0.0.0")


@app.route('/')
def index():
    return "ciao"