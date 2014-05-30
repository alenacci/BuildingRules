import os
import inspect
import module

loc = locals()

modules_classes = []

#load all modules
def load_modules():
	for module_name in os.listdir(os.path.dirname(__file__)):
		if module_name == '__init__.py' or module_name[-3:] != '.py':
			continue
		mod = __import__(module_name[:-3], loc, globals())
		#get all the classes in the module
		for name, obj in inspect.getmembers(mod):
			if inspect.isclass(obj) and obj != module.Module:
				if issubclass(obj, module.Module):
					modules_classes.append(obj)



	del module_name
