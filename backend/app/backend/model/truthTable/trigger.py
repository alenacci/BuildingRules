__author__ = 'andreuke'

class Trigger:
    def __init__(self, trigger):
        self.category = trigger['trigger'].category
        self.params = trigger['translatedParams'] if trigger['translatedParams'] else ""

        # if len(self.params) == 0:
        self.name = trigger['trigger'].triggerName if trigger['trigger'].triggerName else ""

    def getDict(self):
        return self.__dict__

    def __str__(self):
        return str(self.getDict())