__author__ = 'andreuke'

class Action:
    def __init__(self, action):
        self.category = action[1].category
        self.params = action[2]

        if len(self.params) == 0:
            self.params = action[1].actionName

    def compare(self, otherAction):
        #TODO: compare on category
        pass

    def printInfo(self):
        print "ACTION:"
        print self.category
        print self.params
        print "\n"

    #TODO: translate params?