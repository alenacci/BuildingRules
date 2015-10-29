__author__ = 'andreuke'


class Rule:
    def __init__(self, triggers = None, action = None):
        self.triggers = triggers if triggers else []
        self.action = action

    def addTrigger(self, trigger):
        self.triggers.append(trigger)

    def setAction(self, action):
        self.action = action

    def getDict(self):
        triggers = []

        for trigger in self.triggers:
            triggers.append(trigger.getDict())

        return {
            "triggers": triggers,
            "action": self.action.getDict()
        }