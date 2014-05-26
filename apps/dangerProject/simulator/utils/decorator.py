import functools

class decorator(object):

	def __init__(self, f):
		"""
		If there are no decorator arguments, the function
		to be decorated is passed to the constructor.
		"""
		print "Inside __init__()"
		self.f = f

	def __get__(self, instance, instancetype):
		"""Implement the descriptor protocol to make decorating instance
		method possible.

		"""

		# Return a partial function with the first argument is the instance
		#   of the class decorated.
		return functools.partial(self.__call__, instance)

	def __call__(self, *args):
		"""
		The __call__ method is not called until the
		decorated function is called.
		"""
		print "Inside __call__()"
		print args
		self.f(*args)
		print "After self.f(*args)"