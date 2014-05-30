import threading
import simulator
import sys
import time
from triggers.trigger import Trigger

COMMANDS = ['trigger', 'wait', 'quit']
PARAMETERS = {'trigger' : ['name', 'room_id', 'position'],
			  'wait' : ['time'],
			  'quit' : []}

quit = False

def parse_input_for_triggers():
	while not quit:
		input_text = raw_input()
		commands = input_text.split(';')
		for c in commands:
			c = c.strip()
			if len(c) > 0:
				interpret_command(c)

def interpret_command(command):
	words = command.split(" ")
	command_name = words[0]

	if command_name not in COMMANDS:
		print("unrecognized command")
		return

	params = {}

	for w in words[1:]:
		key_value = w.split(':')

		if key_value[0] not in PARAMETERS[command_name]:
			print("not valid parameter: " + key_value[0])
			return

		params[key_value[0]] = key_value[1]

	execute_command(command_name, params)

def execute_command(command_name, params):
	if command_name == 'trigger':

		if not params.has_key('name'):
			print("trigger must have the param \' name \' set")
			return

		t = Trigger(params['name'])
		for k,v in params.iteritems():
			if k != 'name':
				val = int(v) if v.isdigit else v
				t.__setattr__(k,val)

		simulator.sim.trigger_manager.fire_trigger(t)

		print "trigger " + t.name + " executed"

	elif command_name == 'quit':
		global quit
		quit = True
		print "quitting"
	elif command_name == 'wait':
		if params.has_key('time'):
			time.sleep(int(params['time']))
		else:
			print "\'time\' parameter is mandatory"


def start_console():
	console_thread = threading.Thread(target=parse_input_for_triggers)
	console_thread.setDaemon(True)
	console_thread.start()