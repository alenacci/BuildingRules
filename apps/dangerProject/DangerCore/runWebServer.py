#!venv/bin/python
from app import app
import sys
from app.core.dangerCore import *



app.danger_core = DangerCore()
app.danger_core.startConnectionAnalyzer()


app.run(debug = True,port=2001,host="0.0.0.0", use_reloader=False)



