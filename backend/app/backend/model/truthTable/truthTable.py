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

        self.dict = {}
        self.binaryDict = {}
        self.minimizedDict = {}

        rules = room.getRules(includeDisabled=True)
        for rule in rules:
            self.rules[rule.id] = rule

    # Getters
    def getDict(self):
        if not self.dict:
            self.dict = self.makeDict()

        return self.dict

    def getBinarizedTable(self):
        if not self.binaryDict:
            self.binaryDict = self.makeBinarizedTable()

        return self.binaryDict

    def getMinimizedTable(self):
        if not self.minimizedDict:
            self.minimizedDict = self.makeMinimizedTable()

        return self.minimizedDict

    # Make dicts
    def makeDict(self):
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

        return {'rules': rules}

    def makeBinarizedTable(self):
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
            #
            # # Action Intervals
            # if 'translatedParams' in action.keys():
            #     if '0' in action['translatedParams'].keys() and '1' in action['translatedParams'].keys():
            #         if action['category'] not in actionsIntervalsDict:
            #             actionsIntervalsDict[action['category']] = []
            #
            #         intervalList = [d['name'] for d in actionsIntervalsDict[action['category']]]
            #         if action['translatedParams']['0'] not in intervalList:
            #             a = {}
            #             a['name'] = action['translatedParams']['0']
            #             a['description'] = action['description']
            #             actionsIntervalsDict[action['category']].append(a)
            #         if action['translatedParams']['1'] not in intervalList:
            #             a = {}
            #             a['name'] = action['translatedParams']['1']
            #             a['description'] = action['description']
            #             actionsIntervalsDict[action['category']].append(a)
            #
            #     elif '0' in action['translatedParams'].keys():
            #         if action['category'] not in action:
            #             actionsDict[action['category']] = []
            #
            #             actionList = [d['name'] for d in actionsDict[action['category']]]
            #             if action['translatedParams']['0'] not in actionList:
            #                 a = {}
            #                 a['name'] = action['translatedParams']['0']
            #                 a['description'] = action['description']
            #                 actionsDict[action['category']].append(a)
            # # Action Discrete
            # else:
            #     if action['category'] not in actionsDict:
            #         actionsDict[action['category']] = []
            #
            #     actionList = [d['name'] for d in actionsDict[action['category']]]
            #     if action['name'] not in actionList:
            #         a = {}
            #         a['name'] = action['name']
            #         a['description'] = action['description']
            #         actionsDict[action['category']].append(a)


            # TODO: Action not intervalized
            if 'translatedParams' in action.keys():
                if action['category'] not in actionsIntervalsDict:
                    actionsIntervalsDict[action['category']] = []

                actionList = []
                for d in actionsIntervalsDict[action['category']]:
                    if 'translatedParams' in d.keys():
                        name = d['translatedParams']['0']
                        if '1' in d['translatedParams'].keys():
                            name += " - " + d['translatedParams']['1']
                        actionList.append(name)

                actionName = action['translatedParams']['0']

                if '1' in action['translatedParams'].keys():
                    actionName += " - " + action['translatedParams']['1']

                if actionName not in actionList:
                    a = {}
                    a['name'] = actionName
                    a['description'] = action['description']
                    actionsIntervalsDict[action['category']].append(a)
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
            values = self.makeIntervals(value, bounds=key == 'TIME')

            child = self.makeSubCategory(key, values)
            triggerLabels.append(child)

        for key, value in actionsDict.iteritems():
            child = self.makeSubCategory(key, value)
            actionLabels.append(child)

        for key, value in actionsIntervalsDict.iteritems():
            # values = self.makeIntervals(value)

            child = self.makeSubCategory(key, value)
            actionLabels.append(child)

        ruleList = self.getDict()['rules']
        rules = {}

        for r in ruleList:
            triggers = r['triggers']

            ones = self.getOnes(triggers, triggerLabels)
            print triggers
            print ones

            action = r['action']

            if 'translatedParams' in action.keys():
                params = action['translatedParams']
                actionName = params['0']
                if '1' in params.keys():
                    actionName += " - " + params['1']

            else:
                actionName = action['name']
            if actionName not in rules.keys():
                rule = {}
                rule['action'] = actionName
                rule['ones'] = []

                rules[actionName] = rule

            import string
            alphabet = list(string.ascii_lowercase)

            for i in range(len(ones)):
                o = ones[i]

                one = {}
                one['id'] = str(r['id'])
                if (len(ones) > 1):
                    one['id'] += alphabet[i]
                one['enabled'] = r['enabled']
                one['deleted'] = r['deleted']
                one['priority'] = r['priority']
                one['value'] = o

                rules[actionName]['ones'].append(one)

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
            'rules': rules.values()
        }

    def makeMinimizedTable(self):
        binaryDict = self.getBinarizedTable()

        rules = binaryDict['rules']
        labels = binaryDict['labels']

        miniRules = []

        for r in rules:
            rule = {}
            rule['action'] = r['action']

            oldOnes = {d['value']: d for d in r['ones']}
            miniOnes = self.minimize(oldOnes.keys(), labels)

            ones = []

            for o in miniOnes:
                one = {}
                if o in oldOnes:
                    oldOne = oldOnes[o]
                    one['deleted'] = oldOne['deleted']
                    one['enabled'] = oldOne['enabled']
                    one['priority'] = oldOne['priority']
                    one['id'] = oldOne['id']
                    one['value'] = oldOne['value']
                else:
                    one['deleted'] = False
                    one['enabled'] = True
                    one['priority'] = 50
                    one['id'] = 'NEW'
                    one['value'] = o
                ones.append(one)

            rule['ones'] = ones

            miniRules.append(rule)



        return {
            'labels': labels,
            'rules': miniRules
        }



    # Support functions
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

    def makeIntervals(self, value, bounds=False):
        # Sort by dict['name'] inside the list
        entries = sorted(value, key=lambda k: k['name'])

        values = []

        if bounds and entries[0]['name'] != '00':
            first = {}
            first['name'] = '00 - ' + entries[0]['name']
            first['description'] = entries[0]['description']
            params = {}
            params['0'] = '00'
            params['1'] = entries[0]['name']
            first['params'] = params
            values.append(first)


        for i in range(0, len(entries) - 1):
            label = {}
            label['name'] = entries[i]['name'] + " - " + entries[i + 1]['name']
            label['description'] = entries[i]['description']
            params = {}
            params['0'] = entries[i]['name']
            params['1'] = entries[i + 1]['name']
            label['params'] = params

            values.append(label)

        if bounds and entries[-1]['name'] != '23':
            last = {}
            last['name'] = entries[-1]['name'] + " - 23"
            last['description'] = entries[-1]['description']
            params = {}
            params['0'] = entries[-1]['name']
            params['1'] = '23'
            last['params'] = params
            values.append(last)

        return values

    def getOnes(self, triggers, categoryLabels):
        strings = [""]

        for category in categoryLabels:
            cat = category['name']

            children = category['children']

            # Intervals Duplication
            if 'params' in children[0].keys() and '1' in children[0]['params'].keys():
                indexes = []

                for i in range(len(children)):
                    triggerLabel = children[i]
                    values = []
                    for trigger in triggers:
                        if trigger['category'] == cat and 'translatedParams' in trigger.keys():
                            # Same-day interval
                            if trigger['translatedParams']['0'] <= trigger['translatedParams']['1']:
                                if trigger['translatedParams']['0'] <= triggerLabel['params']['0'] and trigger['translatedParams']['1'] >= triggerLabel['params']['1']:
                                    indexes.append(i)
                            # Bound
                            else:
                                if trigger['translatedParams']['0'] <= triggerLabel['params']['0'] and '23' >= triggerLabel['params']['1']\
                                        or '00' <= triggerLabel['params']['0'] and trigger['translatedParams']['1'] >= triggerLabel['params']['1']:
                                    indexes.append(i)

                # Make alternatives
                for i in indexes:
                    value = ''
                    for j in range(len(children)):
                        if j == i:
                            value += '1'
                        else:
                            value += '-'
                    values.append(value)


                # If nothing is present
                if values == []:
                    values = ['-' * len(children)]

                # Append all new alternatives to all other
                newStrings = []
                for v in values:
                    for s in strings:
                        newStrings.append(s + v)
                strings = newStrings

            # Simple name
            else:
                for trigger in children:
                    value = None
                    for t in triggers:
                        if t['category'] == cat:
                            if t['name'] == trigger['name']:
                                value = '1'
                    if value is None:
                        value = '-'

                    for i in range(len(strings)):
                        strings[i] += value

        return strings

    def minimize(self, ones, labels):
        triggersLabels = self.makeTriggerLabels(labels)

        print ''
        print 'Minimizing', ones
        collapsedOnes, dc, indexes = self.getOnesAndDontCares(ones, triggersLabels)
        print collapsedOnes, dc, indexes

        miniOnes = self.__simplify(collapsedOnes, dc=dc)
        print miniOnes

        expandedOnes = self.expandOnes(miniOnes, indexes, len(ones[0]))
        print expandedOnes

        return expandedOnes

    def makeTriggerLabels(self, labels):
        triggerLabels = []

        categories = labels[0]['children']

        for cat in categories:
            triggers = cat['children']

            for t in triggers:
                triggerLabels.append(t['name'])

        return triggerLabels

    def getOnesAndDontCares(self, ones, triggersLabels):

        indexes = []

        # Get non-dc indexes
        for i in range(len(ones[0])):
            for one in ones:
                if one[i] != '-':
                    if i not in indexes:
                        indexes.append(i)

        # Minimize ones dimension
        miniOnes = []
        for one in ones:
            newOne = ""
            for i in indexes:
                newOne += one[i]
            miniOnes.append(newOne)

        # Minimize Labels accordingly
        miniLabels = []
        for i in indexes:
            miniLabels.append(triggersLabels[i])

        dc = self.makeDontCares(miniLabels)

        return miniOnes, dc, indexes

    def makeDontCares(self, labels):
        DCs = []

        domains = []
        domains.append(set(['OCCUPANCY_TRUE', 'OCCUPANCY_FALSE']))
        domains.append(set(['SUNNY', 'RAINY', 'CLOUDY']))

        for domain in domains:
            indexes = []
            if domain.issubset(set(labels)):
                for d in domain:
                    indexes.append(labels.index(d))

            if indexes:
                dc = ""
                for i in range(len(labels)):
                    if i in indexes:
                        dc += "0"
                    else:
                        dc += "-"
                DCs.append(dc)

        return DCs

    def expandOnes(self, ones, indexes, length):
        newOnes = []

        for o in ones:
            one = ""
            count = 0

            for i in range(length):
                if i in indexes:
                    one += o[count]
                    count += 1
                else:
                    one += '-'

            newOnes.append(one)
        return newOnes

    def __simplify(self, ones, dc):
        return self.__tabular(ones, dc)

    def __quineMcCluskey(self, ones, dc):
        from quine_mccluskey.qm import QuineMcCluskey
        qm = QuineMcCluskey()

        return qm.simplify_los(set(ones), set(dc))

    def __tabular(self, ones, dc):
        from app.backend.model.truthTable.quine_mccluskey.driver import *
        return minimize(ones,dc)