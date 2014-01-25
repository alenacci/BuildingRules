import json
import time
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify, Blueprint

from app import app
import rest

gui = Blueprint('gui', __name__, template_folder='templates')

@gui.route('/')
def index():
	return render_template('home.html')

@gui.route('/login/', methods = ['GET', 'POST'])
@gui.route('/login', methods = ['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		response = rest.request("/api/users/<username>/login", {'username' : username, 'password' : password})


		if successResponse(response):
			session["logged_in"] = True
			session["sessionKey"] = response["sessionKey"]
			session["userUuid"] = response["userUuid"]
			session["username"] = username

			return redirect(url_for('gui.index'))
		else:
			error = response['request-errorDescription']

	return render_template('login.html', error=error)	






@gui.route('/logout/')
@gui.route('/logout')
def logout():
	
	if loggedIn():

		response = rest.request("/api/users/<username>/logout", {'username' : session["username"]})

		if successResponse(response):
			del session["logged_in"]
			del session["sessionKey"]
			del session["userUuid"]
			del session["username"]
		else:
			render_template('error.html', error = response['request-errorDescription'])

	return render_template('home.html')	




@gui.route('/buildings/')
@gui.route('/buildings')
def buildings():

	if loggedIn():
		
		response = rest.request("/api/users/<username>/buildings", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

		if successResponse(response):
			return render_template('buildings.html', buildings = response["buildings"])	
		else:
			render_template('error.html', error = response['request-errorDescription'])

	else:
		print "error! you must login beofre"

	return redirect(url_for('gui.login'))





@gui.route('/buildings/<buildingName>/')
@gui.route('/buildings/<buildingName>')
def buildingDetail(buildingName = None):
	if loggedIn():
		
		response = rest.request("/api/users/<username>/buildings/<buildingName>", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

		if successResponse(response):
			return render_template('buildingInfo.html', buildingInfo = response)	
		else:
			render_template('error.html', error = response['request-errorDescription'])

	else:
		print "error! you must login beofre"

	return redirect(url_for('gui.login'))






@gui.route('/buildings/<buildingName>/rooms/')
@gui.route('/buildings/<buildingName>/rooms')
def rooms(buildingName = None):
	if loggedIn():
		
		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

		if successResponse(response):
			roomList = response["rooms"]
			roomRules = {}
			authorList = {}
			groupList = {}


			# Now retrieving room rules
			for room in roomList:
				roomName = room["roomName"]
				response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules", 
					{
					'username' : session["username"],
					'buildingName' : buildingName, 
					'roomName' : roomName,
					'sessionKey' : session["sessionKey"],
					'userUuid' : session["userUuid"],
					'filterByAuthor' : False,
					'includeGroupsRules' : True
					})

				if successResponse(response):
					roomRules[roomName] = response["rules"]
				else:
					render_template('error.html', error = response['request-errorDescription'])
					
				# Getting rules author uuid and groupId. I'll use them later
				for rule in roomRules[roomName]:
					if rule["authorUuid"] not in authorList.keys() and rule["authorUuid"] != session["userUuid"]:
						authorList[rule["authorUuid"]] = None
					if rule["groupId"] and rule["groupId"] not in groupList.keys():
						groupList[rule["groupId"]] = None


			# Getting user info per each stored uuid
			for authorUuid in authorList.keys():
				response = rest.request("/api/users/uuid/<uuid>", {'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

				if successResponse(response):
					authorList[authorUuid] = response
				else:
					render_template('error.html', error = response['request-errorDescription'])

			# Getting group info per each stored groupID
			for groupId in groupList.keys():
				response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>", {'username' : session["username"], 'buildingName' : buildingName, 'groupId' : groupId, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

				if successResponse(response):
					groupList[groupId] = response
				else:
					render_template('error.html', error = response['request-errorDescription'])

			return render_template('rooms.html', roomList = roomList, roomRules = roomRules, authorList = authorList, groupList = groupList)	
		else:
			render_template('error.html', error = response['request-errorDescription'])

	else:
		print "error! you must login beofre"


	return redirect(url_for('gui.login'))


@gui.route('/buildings/<buildingName>/groups/')
@gui.route('/buildings/<buildingName>/groups')
def groups(buildingName = None):
	return render_template('home.html')





@gui.route('/buildings/<buildingName>/rooms/<roomName>rules/add/')
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/add')
def addRuleToRoom(buildingName = None, roomName = None):
	return render_template('ruleForm.html')	

































def loggedIn():

	try:
		if "logged_in" in session.keys() and session["logged_in"]:
			return True
	except:
		pass

	return False


def successResponse(response):
	return response['request-success']	





