from app import app
import sys
import time
import datetime
import json
import logging
from app.backend.commons.errors import *


def checkData(parameters):

	if parameters:
		for parName in parameters.keys():
			if parName != "self":
				
				parVal = parameters[parName]

				if (type(parVal) == str or type(parVal) == unicode) and  "'" in parameters[parName]: raise BadInputError()
				if (type(parVal) == str or type(parVal) == unicode) and  '"' in parameters[parName]: raise BadInputError()