__author__ = 'andreuke'

from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager
from app.backend.commons.console import *
from app.backend.model.rule import Rule
from app.backend.model.room import Room


class TruthTable:
    def __init__(self, room):
        self.room = room
        self.rules = {}

        rules = room.getRules(includeDisabled = True)
        for rule in rules:
            self.rules[rule.id] = rule


    def getDict(self):
        triggerManager = TriggerManager()
        actionManager = ActionManager()

        rules = []

        for id, rule in self.rules.iteritems():
            ruleMin = {}
            ruleMin['id'] = rule.id
            ruleMin['enabled'] = rule.enabled
            ruleMin['deleted'] = rule.deleted
            ruleMin['priority'] = rule.getPriority(roomName=self.room.roomName, buildingName=self.room.buildingName)

            antecedents = triggerManager.translateTrigger(rule.antecedent, getDict=True)
            consequent = actionManager.translateAction(rule.consequent, getDict=True)

            # Triggers
            triggers = self.makeTriggers(antecedents)

            # Action
            action = self.makeAction(consequent)


            ruleMin['triggers'] = triggers
            ruleMin['action'] = action

            rules.append(ruleMin)

        return {'rules':rules}

    def getBinarizedTable(self):
        triggerManager = TriggerManager()
        actionManager = ActionManager()

        triggersDict = {}
        triggersIntervalsDict = {}
        actionsDict = {}
        actionsIntervalsDict = {}

        # HEADERS
        for id, rule in self.rules.iteritems():
            antecedents = triggerManager.translateTrigger(rule.antecedent, getDict=True)
            consequent = actionManager.translateAction(rule.consequent, getDict=True)

            triggers = self.makeTriggers(antecedents)
            action = self.makeAction(consequent)

            for trigger in triggers:
                # Trigger Intervals
                if 'translatedParams' in trigger.keys():
                    if '0' in trigger['translatedParams'].keys() and '1' in trigger['translatedParams'].keys():
                        if trigger['category'] not in triggersIntervalsDict:
                            triggersIntervalsDict[trigger['category']] = []

                        intervalList = [d['name'] for d in triggersIntervalsDict[trigger['category']]]
                        if trigger['translatedParams']['1'] not in intervalList:
                            t = {}
                            t['name'] = trigger['translatedParams']['1']
                            t['description'] = trigger['description']
                            triggersIntervalsDict[trigger['category']].append(t)
                        if trigger['translatedParams']['0'] not in intervalList:
                            t = {}
                            t['name'] = trigger['translatedParams']['0']
                            t['description'] = trigger['description']
                            triggersIntervalsDict[trigger['category']].append(t)
                    elif '0' in trigger['translatedParams'].keys():
                        if trigger['category'] not in triggersDict:
                            triggersDict[trigger['category']] = []

                        triggerList = [d['name'] for d in triggersDict[trigger['category']]]
                        if trigger['translatedParams']['0'] not in triggerList:
                            t = {}
                            t['name'] = trigger['translatedParams']['0']
                            t['description'] = trigger['description']
                            triggersDict[trigger['category']].append(t)

                # Trigger Discrete
                else:
                    if trigger['category'] not in triggersDict:
                        triggersDict[trigger['category']] = []

                    triggerList = [d['name'] for d in triggersDict[trigger['category']]]
                    if trigger['name'] not in triggerList:
                        t = {}
                        t['name'] = trigger['name']
                        t['description'] = trigger['description']
                        triggersDict[trigger['category']].append(t)
            #
            # # Action Intervals
            # if 'translatedParams' in action.keys():
            #     if '0' in action['translatedParams'].keys() and '1' in action['translatedParams'].keys():
            #         if action['category'] not in actionsIntervalsDict:
            #             actionsIntervalsDict[action['category']] = []
            #
            #         intervalList = [d['name'] for d in actionsIntervalsDict[action['category']]]
            #         if action['translatedParams']['0'] not in intervalList:
            #             a = {}
            #             a['name'] = action['translatedParams']['0']
            #             a['description'] = action['description']
            #             actionsIntervalsDict[action['category']].append(a)
            #         if action['translatedParams']['1'] not in intervalList:
            #             a = {}
            #             a['name'] = action['translatedParams']['1']
            #             a['description'] = action['description']
            #             actionsIntervalsDict[action['category']].append(a)
            #
            #     elif '0' in action['translatedParams'].keys():
            #         if action['category'] not in action:
            #             actionsDict[action['category']] = []
            #
            #             actionList = [d['name'] for d in actionsDict[action['category']]]
            #             if action['translatedParams']['0'] not in actionList:
            #                 a = {}
            #                 a['name'] = action['translatedParams']['0']
            #                 a['description'] = action['description']
            #                 actionsDict[action['category']].append(a)
            # # Action Discrete
            # else:
            #     if action['category'] not in actionsDict:
            #         actionsDict[action['category']] = []
            #
            #     actionList = [d['name'] for d in actionsDict[action['category']]]
            #     if action['name'] not in actionList:
            #         a = {}
            #         a['name'] = action['name']
            #         a['description'] = action['description']
            #         actionsDict[action['category']].append(a)


            #TODO: Action not intervalized
            if 'translatedParams' in action.keys():
                if action['category'] not in actionsIntervalsDict:
                    actionsIntervalsDict[action['category']] = []

                actionList = []
                for d in actionsIntervalsDict[action['category']]:
                    if 'translatedParams' in d.keys():
                        name = d['translatedParams']['0']
                        if '1' in d['translatedParams'].keys():
                             name += " - " + d['translatedParams']['1']
                        actionList.append(name)

                actionName = action['translatedParams']['0']

                if '1'in action['translatedParams'].keys():
                    actionName += " - " + action['translatedParams']['1']

                if actionName not in actionList:
                    a = {}
                    a['name'] = actionName
                    a['description'] = action['description']
                    actionsIntervalsDict[action['category']].append(a)
            else:
                if action['category'] not in actionsDict:
                    actionsDict[action['category']] = []

                actionList = [d['name'] for d in actionsDict[action['category']]]
                if action['name'] not in actionList:
                    a = {}
                    a['name'] = action['name']
                    a['description'] = action['description']
                    actionsDict[action['category']].append(a)


        triggerLabels = []
        actionLabels = []

        # Make Intervals
        for key, value in triggersDict.iteritems():
            child = self.makeSubCategory(key, value)
            triggerLabels.append(child)

        for key, value in triggersIntervalsDict.iteritems():
            values = self.makeIntervals(value)

            child = self.makeSubCategory(key, values)
            triggerLabels.append(child)

        for key, value in actionsDict.iteritems():
            child = self.makeSubCategory(key, value)
            actionLabels.append(child)

        for key, value in actionsIntervalsDict.iteritems():
            # values = self.makeIntervals(value)

            child = self.makeSubCategory(key, value)
            actionLabels.append(child)


        ruleList = self.getDict()['rules']
        rules = {}

        for r in ruleList:
            triggers = r['triggers']

            ones = self.getOnes(triggers, triggerLabels)
            print triggers
            print ones

            action = r['action']

            if 'translatedParams' in action.keys():
                params = action['translatedParams']
                actionName = params['0']
                if '1' in params.keys():
                    actionName += " - " + params['1']

            else:
                actionName = action['name']
            if actionName not in rules.keys():
                rule = {}
                rule['action'] = actionName
                rule['ones'] = []

                rules[actionName] = rule

            import string
            alphabet = list(string.ascii_lowercase)

            for i in range(len(ones)):
                o = ones[i]


                one = {}
                one['id'] = str(r['id'])
                if(len(ones) > 1):
                    one['id'] += alphabet[i]
                one['enabled'] = r['enabled']
                one['deleted'] = r['deleted']
                one['priority'] = r['priority']
                one['value'] = o

                rules[actionName]['ones'].append(one)

        labels = []

        triggers = {}
        triggers['name'] = 'Triggers'
        triggers['description'] = ""
        triggers['children'] = triggerLabels

        actions = {}
        actions['name'] = 'Actions'
        actions['description'] = ""
        actions['children'] = actionLabels

        labels.append(triggers)
        labels.append(actions)


        return {
            'labels': labels,
            'rules': rules.values()
        }

    def getMinimizedTable(self):
        # TODO:
        pass

    def makeTriggers(self, antecedents):
        triggers = []

        for trig in antecedents['triggers']:
            t = trig['trigger']

            trigger = {}
            trigger['category'] = t['category']
            trigger['categoryDescription'] = t['description']
            trigger['name'] = t['triggerName']
            trigger['description'] = t['ruleAntecedent']

            if trig['parameterValues']:
                trigger['parameterValues'] = trig['parameterValues']
                trigger['translatedParams'] = trig['translatedParams']

            triggers.append(trigger)
        return triggers

    def makeAction(self, consequent):
        act = consequent['action']

        action = {}
        action['category'] = act['category']
        action['name'] = act['actionName']
        action['description'] = act['description']

        if consequent['translatedParams']:
            action['translatedParams'] = consequent['translatedParams']

        return action

    def makeSubCategory(self, key, value):
        subcategory = {}
        subcategory['name'] = key
        subcategory['description'] = ""

        children = []

        for v in value:
            child = {}
            child['name'] = v['name']
            child['description'] = v['description']
            if 'params' in v.keys():
                child['params'] = v['params']
            children.append(child)

        subcategory['children'] = children

        return subcategory

    def makeIntervals(self, value):
        # Sort by dict['name'] inside the list
        entries = sorted(value, key=lambda k: k['name'])

        values = []
        for i in range(0,len(entries)-1):
            label = {}
            label['name'] = entries[i]['name'] + " - " + entries[i+1]['name']
            label['description'] = entries[i]['description']
            params = {}
            params['0'] = entries[i]['name']
            params['1'] = entries[i+1]['name']
            label['params'] = params

            values.append(label)

        return values

    def getOnes(self, triggers, triggerLabels):
        strings = [""]

        for category in triggerLabels:
            cat = category['name']

            children = category['children']

            # Intervals Duplication
            if 'params' in children[0].keys():
                indexes = []

                for i in range(len(children)):
                    trigger = children[i]
                    values = []
                    for t in triggers:
                        if t['category'] == cat and 'translatedParams' in t.keys():
                            if t['translatedParams']['0'] <= trigger['params']['0'] and t['translatedParams']['1'] >= trigger['params']['1']:
                                indexes.append(i)

                # Make alternatives
                for i in indexes:
                    value = ''
                    for j in range(len(children)):
                        if j == i:
                            value += '1'
                        else:
                            value += '-'
                    values.append(value)


                # If nothing is present
                if values == []:
                    values = ['-' * len(children)]

                # Append all new alternatives to all other
                newStrings = []
                for v in values:
                    for s in strings:
                        newStrings.append(s+v)
                strings = newStrings

            # Simple name
            else:
                for trigger in children:
                    value = None
                    for t in triggers:
                        if t['category'] == cat:
                            if t['name'] == trigger['name']:
                                value = '1'
                    if value == None:
                        value = '-'

                    for i in range(len(strings)):
                        strings[i] += value

        return strings