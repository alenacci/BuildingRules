import json
import time
import requests
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify, Blueprint

from app import app

gui = Blueprint('gui', __name__, template_folder='templates')

@gui.route('/')
def index():
	return render_template('home.html')

@gui.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    
    password = "ciao"
    
    apiRequest(url_for('api.login', username = "ciao"), {'password' : password})
    
    return render_template('login.html', error=error)	

@gui.route('/logout')
def logout():
	return render_template('home.html')	

@gui.route('/buildings')
def buildings():
	return render_template('home.html')	

@gui.route('/buildings/<buildingName>')
def buildingDetail(buildingName = None):
	return render_template('home.html')		

@gui.route('/buildings/<buildingName>/rooms')
def rooms(buildingName = None):
	return render_template('home.html')

@gui.route('/buildings/<buildingName>/groups')
def groups(buildingName = None):
	return render_template('home.html')





def apiRequest(url, data):
	url = "http://" + app.config['HOST_IP'] + ":" + str(app.config['HOST_PORT']) + url
	
	headers = {'Accept-Language': 'en-us', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate'}
	r = requests.post(url, data=json.dumps(data), headers=headers)

	print url
	print r.status_code
	print r.headers
	print r.text


	return None