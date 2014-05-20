#!flask/bin/python
from app import app
from app.core.dangerCore import *


app.danger_core = DangerCore()

app.run(debug = True,port=2001,host="0.0.0.0")
