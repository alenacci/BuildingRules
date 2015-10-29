__author__ = 'andreuke'

class Action:
    def __init__(self, action):
        self.category = action[1].category
        self.params = action[2]

        if len(self.params) == 0:
            self.params = action[1].actionName

    def getDict(self):
        return self.__dict__
