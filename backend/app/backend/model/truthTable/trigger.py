__author__ = 'andreuke'

class Trigger:
    def __init__(self, trigger):
        self.category = trigger['trigger'].category
        self.params = trigger['translatedParams']

        if len(self.params) == 0:
            self.params = trigger['trigger'].triggerName

    def compare(self, otherTrigger):
        #TODO: implementare confronto su category
        pass

    def printInfo(self):
        print "TRIGGER:"
        print self.category
        print self.params
        print "\n"
