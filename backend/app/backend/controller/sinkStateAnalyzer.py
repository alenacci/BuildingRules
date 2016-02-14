__author__ = 'andreuke'
from app.backend.model.room import Room
from app.backend.model.truthTable.truthTable import TruthTable
from app.backend.controller.influenceManager.influenceManager import probability

def sinkStateAnalysis(building, room):
    INFLUENCE_MIN = 0.005
    INFLUENCE_MAX = 0.3

    room = Room(roomName=room, buildingName=building)
    roomRules = room.getRules(includeDisabled=True)
    rulesDescriptions = {int(r.id): 'if ' + r.antecedent + ' then ' + r.consequent for r in roomRules}



    print 'rules'
    print rulesDescriptions

    truthTable = TruthTable(room)
    rules = truthTable.getDict()['rules']
    # print rules

    assertive_rules = {}
    useless_rules = {}

    # SINKS
    actions = {}
    translations = {
        'LIGHT_ON': 'LIGHT_OFF',
        'WINDOWS_OPEN': 'WINDOWS_CLOSE',
        'HVAC_ON': 'HVAC_OFF',
        'COFFEE_ON': 'COFFEE_OFF',
        'PRINTER_ON': 'PRINTER_OFF',
        'COMPUTER_ON': 'COMPUTER_OFF',
        'DESKLIGHT_ON': 'DESKLIGHT_OFF',
        'DISPLAYMONITOR_ON': 'DISPLAYMONITOR_OFF',
        'CURTAINS_OPEN': 'CURTAINS_OFF',
        'PROJECTOR_ON': 'PROJECTOR_OFF',
        'AUDIO_ON': 'AUDIO_OFF',
        'EXHAUST_FAN_ON': 'EXHAUST_FAN_OFF',
        'FUME_HOODS_ON': 'FUME_HOODS_OFF'
    }

    for r in rules:
        priority = float(r['priority'])

        if priority > 1:
            priority /= 100.0

        triggers = r['triggers']

        occupancy = None
        external_temp_min = None
        external_temp_max = None
        weather = None
        room_temp_min = None
        room_temp_max = None
        start_date = None
        end_date = None
        start_time = None
        end_time = None
        day = None

        for t in triggers:
            category = t['category']
            name = t['name']

            if category == 'OCCUPANCY':
                occupancy = True if name == 'OCCUPANCY_TRUE' else False

            elif category == 'TIME':
                start_time = int(t['translatedParams']['0'])
                end_time = int(t['translatedParams']['1'])

            elif category == 'HVAC_TEMP':
                room_temp_min = toCelsius(int(t['translatedParams']['0']))
                room_temp_max = toCelsius(int(t['translatedParams']['1']))

            elif category == 'WEATHER':
                weather = t['description']

            elif category == 'DATE':
                start = t['parameterValues']['0'].split('/')
                end = t['parameterValues']['1'].split('/')

                start_date = start[1] + '-' + start[0]
                end_date = end[1] + '-' + end[0]

            elif category == 'DAY':
                day = t['parameterValues']['0']

            elif category == 'EXT_TEMPERATURE':
                external_temp_min = toCelsius(int(t['translatedParams']['0']))
                external_temp_max = toCelsius(int(t['translatedParams']['1']))

        prob = probability(external_temp_min, external_temp_max, weather, occupancy,
                    room_temp_min, room_temp_max, start_date, end_date,
                    start_time, end_time, day, priority)

        rule = {}
        rule['id'] = r['id']
        rule['influence'] = prob
        rule['description'] = rulesDescriptions[r['id']]

        if prob < INFLUENCE_MIN:
            useless_rules[rule['id']] = rule
        elif prob > INFLUENCE_MAX:
            assertive_rules[rule['id']] = rule


        # SINKS
        action = r['action']['name']

        info = {}
        info['id'] = r['id']
        info['influence'] = prob
        info['description'] = rulesDescriptions[r['id']]

        if action not in actions.keys():
            actions[action] = []
        actions[action].append(info)

    sinks = {}
    semi_sinks = {}

    print actions

    for a, rules in actions.iteritems():
        for r in rules:
            if a in translations.keys():
                opposite = translations[a]

                if opposite not in actions.keys():
                    # r['description'] = getRuleString(r['id'])

                    sinks[r['id']] = r
                else:
                    found = False
                    opposites = []
                    for o in actions[opposite]:
                        if o['influence'] >= INFLUENCE_MIN:
                            found = True
                        opposites.append(o)
                    if not found:
                        # r['description'] = getRuleString(r['id'])
                        r['opposites'] = opposites

                        semi_sinks[r['id']] = r



    # Step 3: Sinks
    actions_to_check = ['windows_open','wake_up_pc','turn on the room light','turn on the printer','turn on my desk light','turn on display monitors']


    # Step 4: Semi-sinks

    response = {}
    response['rules'] = rulesDescriptions
    response['assertive_rules'] = assertive_rules
    response['useless_rules'] = useless_rules
    response['sinks'] = sinks
    response['semi-sinks'] = semi_sinks

    return response


def toCelsius(degree):
    return (degree - 32)*5.0/9.0

def getRuleString(id):
    return id