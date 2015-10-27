__author__ = 'andreuke'

from app.backend.controller.triggerManager import TriggerManager
from app.backend.controller.actionManager import ActionManager
from app.backend.commons.console import *
from app.backend.model.truthTable.trigger import Trigger
from app.backend.model.truthTable.action import Action
from app.backend.model.truthTable.rule import Rule

class TruthTable:
    def __init__(self, room):

        triggerManager = TriggerManager()
        actionManager = ActionManager()

        roomRules = room.getRules()

        self.triggerList = []
        self.actionList = []
        self.rules = []

        for rule in roomRules:
            antecedents = triggerManager.translateTrigger(rule.antecedent)
            consequent = actionManager.translateAction(rule.consequent)

            triggers = []

            for t in antecedents['triggers']:
                trigger = Trigger(t)
                trigger.printInfo()

                if trigger.category not in self.triggerList:
                    self.triggerList.append(trigger.category)

                triggers.append(trigger)

            action = Action(consequent)
            action.printInfo()

            if action.category not in self.actionList:
                self.actionList.append(action.category)

            rule = Rule(triggers, action)
            self.rules.append(rule)

        print self.triggerList
        print self.actionList

        for rule in self.rules:
            rule.printInfo()