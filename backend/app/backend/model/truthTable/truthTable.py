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
            "rules": rules
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


    def getBinarizeddTable(self):
        for