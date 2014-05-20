from app import app
from app.virtualSensorCore import *

app.virtual_sensor_core = VirtualSensorCore()

app.run(debug = True,port=2560,host="0.0.0.0")