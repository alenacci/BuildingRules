from flask import Flask, Blueprint, render_template

app = Flask(__name__)

gui = Blueprint('gui', __name__, template_folder='', static_url_path='', static_folder='')

@gui.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(gui)
