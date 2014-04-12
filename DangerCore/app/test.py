from flask import Flask

app = Flask(__name__)

class Prova:
	def __init__(self):
		self.a = 0

	def foo(self):
		self.a = self.a + 1
		return self.a

p = Prova()

print p.foo()

@app.route('/')
@app.route('/index')
def index():
    return str(p.foo())

app.run(debug = True)
