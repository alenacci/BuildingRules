import sys
import MySQLdb
import string
import random



def createQuery(template, params):
	query = template
	
	for parName in params.keys():
		query = query.replace("@@" + str(parName) + "@@", str(params[parName]))

	return query


queries = []

currentUserUuid = 1
currentGroupId = 1

commonRooms = {}
commonRooms[2107] = "Kitchen"
commonRooms[2144] = "Storage"
commonRooms[3208] = "Conference Room"
commonRooms[2230] = "Study Room"
commonRooms[2109] = "Lobby"

groupA_members = [2108, 2112, 2116, 2111, 2118, 2122, 2126, 2128]
groupB_members = [2203, 2215, 2217, 2231, 2138, 2136, 2134, 2132]

groupA_common = [2140]
groupB_common = [2154]

laboratoryMembers = [2112, 2126, 2138]
laboratoryRoom = 3113


roomOccupancy = {}
roomOccupancy[2108] = 1
roomOccupancy[2112] = 5
roomOccupancy[2116] = 3
roomOccupancy[2111] = 3
roomOccupancy[2118] = 1
roomOccupancy[2122] = 7
roomOccupancy[2126] = 1
roomOccupancy[2128] = 9

roomOccupancy[2203] = 1
roomOccupancy[2215] = 5
roomOccupancy[2217] = 1
roomOccupancy[2231] = 1
roomOccupancy[2138] = 7
roomOccupancy[2136] = 3
roomOccupancy[2134] = 3
roomOccupancy[2132] = 3


thermalZones = [0] * 14
thermalZones[0] = [3113]
thermalZones[1] = [2140]
thermalZones[2] = [2108, 2112]
thermalZones[3] = [2116, 2111]
thermalZones[4] = [2118, 2122]
thermalZones[5] = [2126]
thermalZones[6] = [2128]
thermalZones[7] = [2130]
thermalZones[8] = [2132, 2134]
thermalZones[9] = [2136, 2138, 2231]
thermalZones[10] = [2217, 2215, 2203]
thermalZones[11] = [2154]
thermalZones[12] = [2107, 2144]
thermalZones[13] = [3208]


standardRoomTriggers = []
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 1);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 2);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 5);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 8);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 9);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 10);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 11);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 12);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 13);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 14);")
standardRoomTriggers.append("INSERT INTO `rooms_triggers` (`room_name`, `building_name`, `trigger_id`) VALUES ('@@roomName@@', 'CSE', 15);")

standardRoomActions = []
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 1);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 2);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 3);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 4);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 5);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 6);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 7);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 8);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 9);")
standardRoomActions.append("INSERT INTO `rooms_actions` (`room_name`, `building_name`, `action_id`) VALUES ('@@roomName@@', 'CSE', 10);")


allRooms = commonRooms.keys() + groupA_members + groupB_members + groupA_common + groupB_common + [laboratoryRoom]

queries.append( "TRUNCATE TABLE groups;" )
queries.append( "TRUNCATE TABLE notifications;" )
queries.append( "TRUNCATE TABLE rooms;" )
queries.append( "TRUNCATE TABLE rooms_actions;" )
queries.append( "TRUNCATE TABLE rooms_groups;" )
queries.append( "TRUNCATE TABLE rooms_triggers;" )
queries.append( "TRUNCATE TABLE rules;" )
queries.append( "TRUNCATE TABLE rules_priority;" )
queries.append( "TRUNCATE TABLE sessions;" )
queries.append( "TRUNCATE TABLE users;" )
queries.append( "TRUNCATE TABLE users_rooms;" )
queries.append( "TRUNCATE TABLE active_rules;" )
queries.append( "TRUNCATE TABLE mturk;" )



newRoomSqlTempl = "INSERT INTO `rooms` (`room_name`, `building_name`, `description`) VALUES ('@@roomName@@', 'CSE', '@@description@@');"

for roomName in commonRooms.keys():
	queries.append( createQuery(newRoomSqlTempl, {'roomName': roomName, 'description': commonRooms[roomName]}) )

for roomName in groupA_members + groupB_members:
	queries.append( createQuery(newRoomSqlTempl, {'roomName': roomName, 'description': "Office Room"}) )

for roomName in groupA_common + groupB_common:
	queries.append( createQuery(newRoomSqlTempl, {'roomName': roomName, 'description': "Meeting Room"}) )

queries.append( createQuery(newRoomSqlTempl, {'roomName': laboratoryRoom, 'description': "Laboratory"}) )


for roomName in allRooms:

	for roomTriggerBindSqlTempl in standardRoomTriggers:
		queries.append( createQuery(roomTriggerBindSqlTempl, {'roomName': roomName}) )

	for roomActionBindSqlTempl in standardRoomActions:
		queries.append( createQuery(roomActionBindSqlTempl, {'roomName': roomName}) )



userRoomBindSqlTempl = "INSERT INTO `users_rooms` (`room_name`, `building_name`, `user_uuid`) VALUES ('@@roomName@@', 'CSE', @@userUuid@@);"
createGroupSqlTempl = "INSERT INTO `groups` (`building_name`, `description`, `cross_rooms_validation`, `cross_rooms_validation_categories`) VALUES ('CSE', '@@description@@', @@crossRoomValidation@@, '[@@crossRoomValidationCategories@@]');"
roomGroupBindSqlTempl = "INSERT INTO `rooms_groups` (`group_id`, `building_name`, `room_name`) VALUES (@@groupId@@, 'CSE', '@@roomName@@');"


# Creating the administator
queries.append("INSERT INTO `users` (`username`, `email`, `password`, `person_name`, `level`) VALUES ('admin', 'energybox.buildingrules@gmail.com', 'brulesAdmin2014', 'Administrator', 100);")

for i in range(0,54):
	uuid = currentUserUuid + i
	queries.append("INSERT INTO `users` (`username`, `email`, `password`, `person_name`, `level`) VALUES ('user_" + str(uuid) + "', '--', 'verycomplexpasswordverycomplex-54--$$$-1-2-passwordverycomplexpassword', 'User" + str(uuid) + "', 10);")

	for day in range(0,8):
		token = str(uuid) + "-" + str(day) + "-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
		query = "INSERT INTO `mturk` (`day`, `user_uuid`, `token`) VALUES (@@day@@, @@user_uuid@@, '@@token@@');"
		query = query.replace("@@day@@", str(day))
		query = query.replace("@@user_uuid@@", str(uuid))
		query = query.replace("@@token@@", str(token))
		queries.append(query)

# Adding the administrator to all rooms
for roomName in allRooms:
	queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : roomName, 'userUuid' : currentUserUuid}) )	
currentUserUuid += 1


# Adding the users to the different rooms
for roomName in roomOccupancy.keys():
	for i in range(0, roomOccupancy[roomName]):

		queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : roomName, 'userUuid' : currentUserUuid}) )


		if roomName in groupA_members:
			for r in groupA_common:
				queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : r, 'userUuid' : currentUserUuid}) )

		if roomName in groupB_members:
			for r in groupB_common:
				queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : r, 'userUuid' : currentUserUuid}) )

		if roomName in laboratoryMembers:
			queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : laboratoryRoom, 'userUuid' : currentUserUuid}) )

		for r in commonRooms:
			queries.append( createQuery(userRoomBindSqlTempl, {'roomName' : r, 'userUuid' : currentUserUuid}) )


		currentUserUuid += 1

# Creating the Admin Group
queries.append( createQuery(createGroupSqlTempl, {'description' : 'Administrator Group', 'crossRoomValidation' : 0, 'crossRoomValidationCategories' : ''}) )

# Adding the rooms to the group B
for roomName in allRooms:
	queries.append( createQuery(roomGroupBindSqlTempl, {'groupId': currentGroupId, 'roomName': roomName}) )
currentGroupId += 1

# Creating the group A
queries.append( createQuery(createGroupSqlTempl, {'description' : 'Room Group A', 'crossRoomValidation' : 0, 'crossRoomValidationCategories' : ''}) )

# Adding the rooms to the group B
for roomName in groupA_members:
	queries.append( createQuery(roomGroupBindSqlTempl, {'groupId': currentGroupId, 'roomName': roomName}) )
currentGroupId += 1


# Creating the group B
queries.append( createQuery(createGroupSqlTempl, {'description' : 'Room Group B', 'crossRoomValidation' : 0, 'crossRoomValidationCategories' : ''}) )

# Adding the rooms to the group B
for roomName in groupB_members:
	queries.append( createQuery(roomGroupBindSqlTempl, {'groupId': currentGroupId, 'roomName': roomName}) )
currentGroupId += 1


heatingString = '"HEATING"'

# Creating the thermal zones
thZonesCount = 1
for i in range(0, len(thermalZones)):
	if len(thermalZones[i]) > 1:
		queries.append( createQuery(createGroupSqlTempl, {'description' : 'Thermal Zone ' + str(thZonesCount), 'crossRoomValidation' : 1, 'crossRoomValidationCategories' : heatingString}) )
		for roomName in thermalZones[i]:
			queries.append( createQuery(roomGroupBindSqlTempl, {'groupId': currentGroupId, 'roomName': roomName}) )
		currentGroupId += 1
		thZonesCount += 1




con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'buildingdepot', db = 'building_rules')
cur = con.cursor()

for q in queries:
	print q
	cur.execute(q)
	con.commit()


con.close()
