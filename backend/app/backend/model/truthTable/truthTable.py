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

            # Action Intervals
            if 'translatedParams' in action.keys():
                if '0' in action['translatedParams'].keys() and '1' in action['translatedParams'].keys():
                    if action['category'] not in actionsIntervalsDict:
                        actionsIntervalsDict[action['category']] = []

                    intervalList = [d['name'] for d in actionsIntervalsDict[action['category']]]
                    if action['translatedParams']['0'] not in intervalList:
                        a = {}
                        a['name'] = action['translatedParams']['0']
                        a['description'] = action['description']
                        actionsIntervalsDict[action['category']].append(a)
                    if action['translatedParams']['1'] not in intervalList:
                        a = {}
                        a['name'] = action['translatedParams']['1']
                        a['description'] = action['description']
                        actionsIntervalsDict[action['category']].append(a)

                elif '0' in action['translatedParams'].keys():
                    if action['category'] not in action:
                        actionsDict[action['category']] = []

                        actionList = [d['name'] for d in actionsDict[action['category']]]
                        if action['translatedParams']['0'] not in actionList:
                            a = {}
                            a['name'] = action['translatedParams']['0']
                            a['description'] = action['description']
                            actionsDict[action['category']].append(a)
            # Action Discrete
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
            values = self.makeIntervals(value)

            child = self.makeSubCategory(key, values)
            actionLabels.append(child)


        rules = self.getDict()['rules']

        for r in rules:
            triggers = r['triggers']

            ones = self.getOnes(triggers, triggerLabels)
            print triggers
            print ones




        # # RULES
        # rules = []
        #
        # for r in self.rules:
        #     triggers = []
        #     for trigger in r.triggers:
        #         if trigger.category in triggersIntervalsDict:
        #             intervals = triggersIntervalsDict[trigger.category]
        #             for i in range(0, len(intervals)-1):
        #                 if int(intervals[i]) >= int(trigger.params['0']) and int(intervals[i+1]) <= int(trigger.params['1']):
        #                     interval = intervals[i] + " - " + intervals[i+1]
        #                     triggers.append({'super-category': trigger.category, 'category': interval, 'name': 1, 'params': ''})
        #         elif trigger.category in triggersDict:
        #             triggers.append({'super-category': trigger.category, 'category': trigger.name, 'name': 1, 'params': ''})
        #
        #     action = None
        #     if r.action.category in actionsIntervalsDict:
        #         intervals = actionsIntervalsDict[r.action.category]
        #         for i in range(0, len(intervals) - 1):
        #             if int(intervals[i]) >= int(r.action.params['0']) and int(intervals[i+1]) <= int(r.action.params['1']):
        #                 interval = intervals[i] + " - " + intervals[i+1]
        #                 action = {'super-category': r.action.category, 'category': interval, 'name': 1, 'params': ''}
        #     elif r.action.category in actionsDict:
        #             action = {'super-category': r.action.category, 'category': r.action.name, 'name': 1, 'params': ''}
        #
        #     rules.append({'action': action, 'triggers': triggers})

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
        }

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
        # values.append("<" + entries[0])
        for i in range(0,len(entries)-1):
            label = {}
            label['name'] = entries[i]['name'] + " - " + entries[i+1]['name']
            label['description'] = entries[i]['description']
            params = {}
            params['0'] = entries[i]['name']
            params['1'] = entries[i+1]['name']
            label['params'] = params

            values.append(label)
        # values.append(entries[-1] + ">")

        return values

    def getOnes(self, triggers, triggerLabels):
        string = ""


        for category in triggerLabels:
            cat = category['name']
            for trigger in category['children']:
                value = None
                for t in triggers:
                    if t['category'] == cat:
                        if t['name'] == trigger['name']:
                            value = '1'
                        if 'translatedParams' in t.keys() and 'params' in trigger.keys():
                            if t['translatedParams']['0'] <= trigger['params']['0'] and t['translatedParams']['1'] >= trigger['params']['1']:
                                value = '1'
                if value == None:
                    value = '-'
                string += value
        return string

