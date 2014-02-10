import json
import time
from flask import request, session, g, redirect, url_for, abort, render_template, flash, jsonify, Blueprint

from app import app
import rest

gui = Blueprint('gui', __name__, template_folder='templates')

@gui.route('/')
def index():

	if loggedIn():
		return redirect(url_for('gui.buildings'))

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
			

			response = rest.request("/api/users/<username>", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
			if not successResponse(response): render_template('error.html', error = response['request-errorDescription'])
			session["userLevel"] = response["level"]
			session["userEmail"] = response["email"]

			response = rest.request("/api/users/<username>/buildings", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
			if not successResponse(response): render_template('error.html', error = response['request-errorDescription'])
			session["buildings"] = response["buildings"]

			return redirect(url_for('gui.index'))
		else:
			error = response['request-errorDescription']

	return render_template('login.html', error=error)	






@gui.route('/logout/')
@gui.route('/logout')
def logout():
	
	if loggedIn():

		response = rest.request("/api/users/<username>/logout", {'username' : session["username"]})

		del session["logged_in"]
		del session["sessionKey"]


		if successResponse(response):
			del session["userUuid"]
			del session["username"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])

	return render_template('home.html')	




@gui.route('/buildings/')
@gui.route('/buildings')
def buildings():

	if not loggedIn():	return redirect(url_for('gui.login'))
		
	response = rest.request("/api/users/<username>/buildings", {'username' : session["username"], 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	if "buildings" not in response.keys():
		return render_template('error.html', error = response['request-errorDescription'])		

	if len(response["buildings"]) == 1:
		buildingName = response["buildings"][0]["buildingName"]
		return redirect(url_for('gui.buildingDetail', buildingName = buildingName))		

	return render_template('buildings.html', buildings = response["buildings"])	


	





@gui.route('/buildings/<buildingName>/')
@gui.route('/buildings/<buildingName>')
def buildingDetail(buildingName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if int(session["userLevel"]) < 100:
		return redirect(url_for('gui.rooms', buildingName = buildingName))
		
	response = rest.request("/api/users/<username>/buildings/<buildingName>", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if successResponse(response):
		return render_template('buildingInfo.html', buildingInfo = response)	
	else:
		return render_template('error.html', error = response['request-errorDescription'])






@gui.route('/buildings/<buildingName>/rooms/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms', methods = ['GET', 'POST'])
def rooms(buildingName = None):
	
	if not loggedIn():	return redirect(url_for('gui.login'))


	##################################
	# Retrieving the rules categories
	##################################
	response = rest.request("/api/users/<username>/rules/categories", {
		'username' : session["username"], 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	categories = response['categories']

	categoriesFilterList = []
	# CREATING THE LIST OF THE CHOSEN CATEGORIES
	for category in categories:
		currentKey = 'filter_by_' + category
		if currentKey in request.form.keys():
			if request.form[currentKey] == "True":
				categoriesFilterList.append(category)

	if len(categoriesFilterList) == 0:
		categoriesFilter = None
	else:
		categoriesFilter = json.dumps(categoriesFilterList, separators=(',',':'))
			
	print ">>>>>>>>>>>>"
	print categoriesFilterList
	print categoriesFilter

	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	notificationList = []
	roomList = response["rooms"]
	roomRules = {}
	authorList = {}
	groupList = {}
	triggerList = {}
	actionList = {}
	userList = {}
	roomGroupList = {}


	# Getting notifications
	response = rest.request("/api/users/<username>/notifications", 
		{
		'username' : session["username"],
		'sessionKey' : session["sessionKey"],
		'userUuid' : session["userUuid"]
		})

	if successResponse(response):
		notificationList = response["notifications"]
	else:
		return render_template('error.html', error = response['request-errorDescription'])


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
			'includeGroupsRules' : True,
			'orderByPriority' : True,
			'categoriesFilter' : categoriesFilter
			})

		if successResponse(response):
			roomRules[roomName] = response["rules"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/users", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : True
			})

		if successResponse(response):
			userList[roomName] = response["users"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/groups", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : True
			})

		if successResponse(response):
			roomGroupList[roomName] = response["groups"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/triggers", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : True
			})

		if successResponse(response):
			triggerList[roomName] = response["triggers"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])



		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/actions", 
			{
			'username' : session["username"],
			'buildingName' : buildingName, 
			'roomName' : roomName,
			'sessionKey' : session["sessionKey"],
			'userUuid' : session["userUuid"],
			'filterByAuthor' : False,
			'includeGroupsRules' : True,
			'orderByPriority' : True
			})

		if successResponse(response):
			print
			print 
			print
			print response
			actionList[roomName] = response["actions"]
		else:
			return render_template('error.html', error = response['request-errorDescription'])


			
		# Getting rules author uuid and groupId. I'll use them later
		for rule in roomRules[roomName]:
			if rule["authorUuid"] not in authorList.keys() and rule["authorUuid"] != session["userUuid"]:
				authorList[rule["authorUuid"]] = None
			if rule["groupId"] and rule["groupId"] not in groupList.keys():
				groupList[rule["groupId"]] = None


	# Getting user info per each stored uuid
	for authorUuid in authorList.keys():
		response = rest.request("/api/users/uuid/<uuid>", {'sessionKey' : session["sessionKey"], 'uuid' : authorUuid, 'userUuid' : session["userUuid"]})

		if successResponse(response):
			authorList[authorUuid] = response
		else:
			return render_template('error.html', error = response['request-errorDescription'])

	
	# Getting group info per each stored groupID
	for groupId in groupList.keys():
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>", {'username' : session["username"], 'buildingName' : buildingName, 'groupId' : groupId, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})

		if successResponse(response):
			groupList[groupId] = response
		else:
			return render_template('error.html', error = response['request-errorDescription'])


	return render_template('rooms.html', roomList = roomList, roomRules = roomRules, authorList = authorList, groupList = groupList, triggerList = triggerList, actionList = actionList, userList = userList, roomGroupList = roomGroupList, notificationList = notificationList, categories = categories, categoriesFilter = categoriesFilter)	


@gui.route('/buildings/<buildingName>/groups/')
@gui.route('/buildings/<buildingName>/groups')
def groups(buildingName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups", {
		'username' : session["username"], 
		'buildingName' : buildingName, 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	groupList = response["groups"]
	roomsGroup = {}
	rulesGroup = {}
	authorList = {}

	for group in groupList:

		# Getting the room list per each group
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'groupId' : group['id'],
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})


		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		if response["rooms"]:
			roomsGroup[group['id']] = response["rooms"]


		# Getting the rule list per each group
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'groupId' : group['id'],
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})


		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		if response["rules"]:
			rulesGroup[group['id']] = response["rules"]

			for rule in rulesGroup[group['id']]:
				if rule["authorUuid"] not in authorList.keys() and rule["authorUuid"] != session["userUuid"]:
					authorList[rule["authorUuid"]] = None

		# Getting user info per each stored uuid
		for authorUuid in authorList.keys():
			response = rest.request("/api/users/uuid/<uuid>", {'sessionKey' : session["sessionKey"], 'uuid' : authorUuid, 'userUuid' : session["userUuid"]})

			if successResponse(response):
				authorList[authorUuid] = response
			else:
				return render_template('error.html', error = response['request-errorDescription'])


	return render_template('groups.html', groupList = groupList, roomsGroup = roomsGroup, rulesGroup = rulesGroup, authorList = authorList)
		

@gui.route('/buildings/<buildingName>/groups/<groupId>/')
@gui.route('/buildings/<buildingName>/groups/<groupId>')
def groupDetail(buildingName = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))
	
	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>", {'groupId' : groupId, 'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
	if not successResponse(response): return render_template('error.html', error = response['request-errorDescription'])
	groupInfo = response

	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms", {'groupId' : groupId, 'username' : session["username"], 'buildingName' : buildingName, 'sessionKey' : session["sessionKey"], 'userUuid' : session["userUuid"]})
	if not successResponse(response): return render_template('error.html', error = response['request-errorDescription'])
	rooms = response["rooms"]
	
	return render_template('groupInfo.html', groupInfo = groupInfo, rooms = rooms)	
		


@gui.route('/buildings/<buildingName>/groups/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/add', methods = ['GET', 'POST'])
def addGroup(buildingName = None):


	if not loggedIn():	return redirect(url_for('gui.login'))

	##################################
	# Retrieving the building roomList
	##################################
	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms", {
		'username' : session["username"], 
		'buildingName' : buildingName, 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])
	
	roomList = response["rooms"]


	##################################
	# Retrieving the rules categories
	##################################
	response = rest.request("/api/users/<username>/rules/categories", {
		'username' : session["username"], 
		'sessionKey' : session["sessionKey"], 
		'userUuid' : session["userUuid"]
	})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	categories = response['categories']


	##################################
	# Now manaing POST and GET requests
	##################################

	if request.method == 'GET':
		return render_template('groupForm.html', roomList = roomList, categories = categories)

	elif request.method == 'POST':

		description = request.form['description']
		crossRoomsValidation = request.form['crossRoomsValidation'] if 'crossRoomsValidation' in request.form.keys() else False
		crossRoomsValidationCategories = []


		# CREATING THE LIST OF THE CHOSEN CATEGORIES
		for category in categories:
			currentKey = 'filter_by_' + category
			if currentKey in request.form.keys():
				if request.form[currentKey] == "True":
					crossRoomsValidationCategories.append(category)

		# NOW STORING THE NEW GROUP
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/add", {
			'username' : session["username"], 
			'buildingName' : buildingName, 
			'description' : description,
			'crossRoomsValidation' : crossRoomsValidation,
			'crossRoomsValidationCategories' : json.dumps(crossRoomsValidationCategories, separators=(',',':')),
			'sessionKey' : session["sessionKey"], 
			'userUuid' : session["userUuid"]
		})

		if not successResponse(response):
			return render_template('error.html', error = response['request-errorDescription'])

		# now let us add each selected room to the created group
		groupId = response['id']

		# NOW ADDING EACH SELECTED ROOM TO THE CREATED GROUP
		for room in roomList:

			if ("room_" + room["roomName"]) in request.form.keys():
				response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/add", {
					'username' : session["username"], 
					'buildingName' : buildingName, 
					'groupId' : groupId,
					'roomName' : room["roomName"],
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
				})

				if not successResponse(response):
					return render_template('error.html', error = response['request-errorDescription'])		


		return redirect(url_for('gui.groups', buildingName = buildingName))

	





@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/add', methods = ['GET', 'POST'])
def addRuleToRoom(buildingName = None, roomName = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':


		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

		
		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/add", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})


		if successResponse(response):
			flash("The rule has been added correctly!")
			return redirect(url_for('gui.rooms', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForRoom = True)

	else:
		return render_template('ruleForm.html', insertionForRoom = True)	


@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/add/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/add', methods = ['GET', 'POST'])
def addRuleToGroup(buildingName = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':


		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

		
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/add", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})


		if successResponse(response):
			flash("The rule has been added correctly!")
			return redirect(url_for('gui.groups', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForGroup = True)

	else:
		return render_template('ruleForm.html', insertionForGroup = True)	



@gui.route('/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rooms/<roomName>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
def editRoomRule(buildingName = None, roomName = None, ruleId = None, groupId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':

		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

	
		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/edit", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})
		
		
		if successResponse(response):
			flash("The rule has been saved correctly!")
			return redirect(url_for('gui.rooms', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForRoom = True)

	else:

		response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'roomName' : roomName,
					'ruleId' : ruleId,
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})

		if not successResponse(response):
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForRoom = True)

		rule = response


		return render_template('ruleForm.html', rule = rule, insertionForRoom = True)



@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable', methods = ['GET'])
def disableRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/disable", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.rooms', buildingName = buildingName))


@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable', methods = ['GET'])
def enableRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/enable", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.rooms', buildingName = buildingName))


@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete', methods = ['GET'])
def deleteRoomRule(buildingName = None, roomName = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/rooms/<roomName>/rules/<ruleId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'roomName' : roomName,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.rooms', buildingName = buildingName))




@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit/', methods = ['GET', 'POST'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit', methods = ['GET', 'POST'])
def editGroupRule(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	if request.method == 'POST':

		ruleBody = request.form['ruleBody']
		priority = request.form['priority']

	
		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/edit", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'priority' : priority, 
					'ruleBody' : ruleBody, 
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})
		
		
		if successResponse(response):
			flash("The rule has been saved correctly!")
			return redirect(url_for('gui.groups', buildingName = buildingName))
		else:
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForGroup = True)

	else:

		response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>", {
					'username' : session["username"],
					'buildingName' : buildingName,
					'groupId' : groupId,
					'ruleId' : ruleId,
					'sessionKey' : session["sessionKey"], 
					'userUuid' : session["userUuid"]
					})

		if not successResponse(response):
			return render_template('ruleForm.html', error = response['request-errorDescription'], insertionForGroup = True)

		rule = response


		return render_template('ruleForm.html', rule = rule, insertionForGroup = True)





@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete', methods = ['GET'])
def deleteGroupRule(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))


	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/rules/<ruleId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'groupId' : groupId,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.groups', buildingName = buildingName))




@gui.route('/buildings/<buildingName>/groups/<groupId>/delete/', methods = ['GET'])
@gui.route('/buildings/<buildingName>/groups/<groupId>/delete', methods = ['GET'])
def deleteGroup(buildingName = None, groupId = None, ruleId = None):

	if not loggedIn():	return redirect(url_for('gui.login'))

	response = rest.request("/api/users/<username>/buildings/<buildingName>/groups/<groupId>/delete", {
				'username' : session["username"],
				'buildingName' : buildingName,
				'groupId' : groupId,
				'ruleId' : ruleId,
				'sessionKey' : session["sessionKey"], 
				'userUuid' : session["userUuid"]
				})

	if not successResponse(response):
		return render_template('error.html', error = response['request-errorDescription'])

	rule = response


	return redirect(url_for('gui.groups', buildingName = buildingName))







def loggedIn():

	try:
		if "logged_in" in session.keys() and session["logged_in"]:
			return True
	except:
		pass

	return False


def successResponse(response):
	return response['request-success']	





