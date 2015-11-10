__author__ = 'andreuke'

class Action:
    def __init__(self, action):
        self.category = action[1].category
        self.params = action[2] if action[2] else ""

        self.name = action[1].actionName if action[1].actionName else ""

    def getDict(self):
        return self.__dict__
