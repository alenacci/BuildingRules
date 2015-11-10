__author__ = 'andreuke'

from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager
from app.backend.commons.console import *
from app.backend.model.truthTable.trigger import Trigger
from app.backend.model.truthTable.action import Action
from app.backend.model.truthTable.rule import Rule

class TruthTable:
    def __init__(self, room):
        self.rules = []

        print room

        triggerManager = TriggerManager()
        actionManager = ActionManager()

        roomRules = room.getRules(includeDisabled = True)

        for rule in roomRules:
            antecedents = triggerManager.translateTrigger(rule.antecedent)
            consequent = actionManager.translateAction(rule.consequent)

            triggers = []

            # TODO: add Meta-info
            for t in antecedents['triggers']:
                trigger = Trigger(t)
                triggers.append(trigger)

            action = Action(consequent)

            rule = Rule(triggers, action)
            self.rules.append(rule)

        # print self.triggerList
        # print self.actionList
        #
        # for rule in self.rules:
        #     rule.printInfo()

    def getDict(self):
        labels = self.getLabels()
        rules = []

        for rule in self.rules:
            rules.append(rule.getDict())

        return {
            "triggerLabels": labels["triggers"],
            "actionLabels": labels["actions"],
            "rules": rules,
            "binary": False

        }

    def getLabels(self):
        triggerLabels = []
        actionLabels = []

        for rule in self.rules:
            for trigger in rule.triggers:
                if trigger.category not in triggerLabels:
                    triggerLabels.append(trigger.category)
            if rule.action.category not in actionLabels:
                actionLabels.append(rule.action.category)

        return {
            "triggers": triggerLabels,
            "actions": actionLabels
        }

    def getBinarizedTable(self):
        triggersDict = {}
        triggersIntervalsDict = {}
        actionsDict = {}
        actionsIntervalsDict = {}

        # Fill dictionaries
        for rule in self.rules:
            for trigger in rule.triggers:

                if trigger.params != "":
                    if trigger.category not in triggersIntervalsDict:
                        triggersIntervalsDict[trigger.category] = []
                    if trigger.params['0'] not in triggersIntervalsDict[trigger.category]:
                        triggersIntervalsDict[trigger.category].append(trigger.params['0'])
                    if trigger.params['1'] not in triggersIntervalsDict[trigger.category]:
                        triggersIntervalsDict[trigger.category].append(trigger.params['1'])
                else:
                    if trigger.category not in triggersDict:
                        triggersDict[trigger.category] = []
                    if trigger.name not in triggersDict[trigger.category]:
                        triggersDict[trigger.category].append(trigger.name)


            if rule.action.params != "":
                if rule.action.category not in actionsIntervalsDict:
                    actionsIntervalsDict[rule.action.category] = []
                if rule.action.params['0'] not in actionsIntervalsDict[rule.action.category]:
                    actionsIntervalsDict[rule.action.category].append(rule.action.params['0'])
                if rule.action.params['1'] not in actionsIntervalsDict[rule.action.category]:
                    actionsIntervalsDict[rule.action.category].append(rule.action.params['1'])
            else:
                if rule.action.category not in actionsDict:
                    actionsDict[rule.action.category] = []
                if rule.action.name not in actionsDict[rule.action.category]:
                    actionsDict[rule.action.category].append(rule.action.name)

        triggerLabels = []
        actionLabels = []

        # Make Intervals
        for key, value in triggersDict.iteritems():
            triggerLabels.append({'category': key, 'values': value})

        for key, value in triggersIntervalsDict.iteritems():
            entries = value

            entries.sort()

            # TODO: strict less and greater

            values = []
            values.append("<" + entries[0])
            for i in range(0,len(entries)-1):
                values.append(entries[i] + " - " + entries[i+1])
            values.append(entries[-1] + ">")

            triggerLabels.append({'category': key, 'values': values})

        for key, value in actionsDict.iteritems():
            actionLabels.append({'category': key, 'values': value})

        for key, value in actionsIntervalsDict.iteritems():
            entries = value

            entries.sort()

            # TODO: strict less and greater

            values = []
            values.append("<" + entries[0])
            for i in range(0,len(entries)-1):
                values.append(entries[i] + " - " + entries[i+1])
            values.append(entries[-1] + ">")

            actionLabels.append({'category': key, 'values': values})

        rules = []

        for r in self.rules:
            triggers = []
            for trigger in r.triggers:
                if trigger.category in triggersIntervalsDict:
                    intervals = triggersIntervalsDict[trigger.category]
                    for i in range(0, len(intervals)-1):
                        if int(intervals[i]) >= int(trigger.params['0']) and int(intervals[i+1]) <= int(trigger.params['1']):
                            interval = intervals[i] + " - " + intervals[i+1]
                            triggers.append({'super-category': trigger.category, 'category': interval, 'name': 1, 'params': ''})
                elif trigger.category in triggersDict:
                    triggers.append({'super-category': trigger.category, 'category': trigger.name, 'name': 1, 'params': ''})

            action = None
            if r.action.category in actionsIntervalsDict:
                intervals = actionsIntervalsDict[r.action.category]
                for i in range(0, len(intervals) - 1):
                    if int(intervals[i]) >= int(r.action.params['0']) and int(intervals[i+1]) <= int(r.action.params['1']):
                        interval = intervals[i] + " - " + intervals[i+1]
                        action = {'super-category': r.action.category, 'category': interval, 'name': 1, 'params': ''}
            elif r.action.category in actionsDict:
                    action = {'super-category': r.action.category, 'category': r.action.name, 'name': 1, 'params': ''}

            rules.append({'action': action, 'triggers': triggers})

        return {
            'triggerLabels': triggerLabels,
            'actionLabels': actionLabels,
            'rules': rules,
            'binary': True
        }


