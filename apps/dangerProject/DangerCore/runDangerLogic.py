#!venv/bin/python
from app import app
from app.core.dangerCore import *

app.danger_core = DangerCore()
app.danger_core.startConnectionAnalyzer()


