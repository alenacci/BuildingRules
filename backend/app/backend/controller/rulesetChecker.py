import os
import sys
import subprocess
import random
import string

from app.backend.model.rule import Rule


class RulesetChecker:

	def __init__(self, ruleList):

		# TAGS
		self.__ROOMTAG = "#ROOMTAG#"

		# Constant strins definition
		self.__OCCUPACY_PRESENT = "(inRoom" + " " + self.__ROOMTAG + ")"
		self.__TEMPERATURE = "(tempInRoom" +  " " + self.__ROOMTAG + ")"
		self.__LIGHT_ON = "(light" + " " + self.__ROOMTAG + ")"
		self.__HEATING_ON = "(heat" + " " + self.__ROOMTAG + ")"
		self.__TIME = "(time" +  " " + self.__ROOMTAG + ")"
		self.__DAY = "(day" +  " " + self.__ROOMTAG + ")"
		self.__SUNNY = "(sunny" + " " + self.__ROOMTAG + ")"
		self.__RAINY = "(rainy" + " " + self.__ROOMTAG + ")"
		self.__POWER_SOCKET_ON = "socket"


		self.__TEMPERATURE_TOKEN = self.__TEMPERATURE.replace(self.__ROOMTAG, "").replace("(","").replace(")","").strip()
		self.__TIME_TOKEN = self.__TIME.replace(self.__ROOMTAG, "").replace("(","").replace(")","").strip()

		# Initializing input rule set list
		self.specified_rules = []
		for rule in ruleList:
			ruleStr = rule.getStandardRepresentation().replace(" group ", " room ")
			self.specified_rules.append(self.analyzeInputRulesFileLine(ruleStr))



		self.dynamic_declaration = []
		self.rooms_list = []

		self.months_token = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

		self.__MAIN_PATH = "tools/z3/"
		self.errorList = []

		# Rules priority
		# date
		# weather
		# presence
		# time

	def isDateAntecedent(self, the_antecedent):
		for m in self.months_token:
			if m in the_antecedent:
				return True
		return False

	def antecedentTranslation(self, the_antecedent):

		ant = the_antecedent

		if ant.startswith("someone is")												: return self.__OCCUPACY_PRESENT
		if ant.startswith("anyone is") 												: return "(not " + self.__OCCUPACY_PRESENT + ")"
		if ant.startswith("temperature is higher than")								: return (ant.replace("temperature is higher than", "(> " + self.__TEMPERATURE + " ") + ")" )
		if ant.startswith("temperature is lower than")								: return (ant.replace("temperature is lower than", "(< " + self.__TEMPERATURE + " ")  + ")" )
		if ant.startswith("temperature is equal to")								: return (ant.replace("temperature is equal to", "(= " + self.__TEMPERATURE + " ")  + ")" )
		if ant.startswith("temperature is between")									: return (ant.replace("and"," " + self.__TEMPERATURE + ") (< " + self.__TEMPERATURE + " ").replace("temperature is between",  "(and (< ")  + "))" )
		if ant.startswith("it is after") and ("AM" in ant or "PM" in ant)			: return (ant.replace("it is after", "(> " + self.__TIME + " ")  + ")" )
		if ant.startswith("it is before") and ("AM" in ant or "PM" in ant)			: return (ant.replace("it is before", "(< " + self.__TIME + " ")  + ")" )
		if ant.startswith("it is between")  and ("AM" in ant or "PM" in ant)		: return (ant.replace("and"," " + self.__TIME + ") (< " + self.__TIME + " ").replace("it is between",  "(and (< ")  + "))" )	
		if ant.startswith("it is") and "o'clock" in ant 							: return (ant.replace("it is ", "(= " + self.__TIME + " ").replace("o'clock", "")  + ")" )
		if ant.startswith("it is after") and self.isDateAntecedent(ant) 			: return (ant.replace("it is after", "(> " + self.__DAY + " ")  + ")" )
		if ant.startswith("it is before") and self.isDateAntecedent(ant) 			: return (ant.replace("it is before", "(< " + self.__DAY + " ")  + ")" )
		if ant.startswith("it is between") and self.isDateAntecedent(ant)			: return (ant.replace("and"," " + self.__DAY + ") (< " + self.__DAY + " ").replace("it is between",  "(and (< ")  + "))" )	
		if ant.startswith("it is") and self.isDateAntecedent(ant) 					: return (ant.replace("it is ", "(= " + self.__DAY + " ")  + ")" )
		if ant.startswith("it is sunny") 											: return self.__SUNNY
		if ant.startswith("it is rainy") 											: return self.__RAINY
		

		error = "Unsupported antecedent: " + the_antecedent
		print error
		self.errorList.append(error)
		return the_antecedent


	def consequentTranslation(self, the_consequent):

		if the_consequent.startswith("turn on the light")				: return self.__LIGHT_ON
		if the_consequent.startswith("turn off the light")				: return "(not " + self.__LIGHT_ON + ")"
		if the_consequent.startswith("turn on the heating")				: return self.__HEATING_ON
		if the_consequent.startswith("turn off the heating")			: return "(not " + self.__HEATING_ON + ")"
		if the_consequent.startswith("turn on the power socket")		: return the_consequent.replace("turn on the power socket ", self.__POWER_SOCKET_ON).replace(" ","")
		if the_consequent.startswith("turn off the power socket")		: return "(not " + the_consequent.replace("turn off the power socket ", self.__POWER_SOCKET_ON).replace(" ","") + ")"


		error = "Unsupported consequent: " + the_consequent
		print error
		self.errorList.append(error)
		return the_consequent


	def analyzeInputRulesFileLine(self, the_line):
			print "Analyzing rule: '" + the_line.replace("\n","") + "'"
			the_line = the_line.replace("if ", "")
			splt_line = the_line.split(" in ")
			antecedent = splt_line[0].strip()
			
			splt_line = splt_line[1].split(" then ")
			location = splt_line[0].strip().replace("room", "").strip()
			consequent = splt_line[1].strip()

			result = [antecedent, consequent, location]

			return result

	def filterSpecifiedRulesByLocation(self, the_location):
		filtered_self.specified_rules = []
		
		for rule in self.specified_rules:
			if rule[2] == the_location:
				filtered_self.specified_rules.append(rule)

		return filtered_self.specified_rules


	def correctTime(self, statement):

		if "time" not in statement:
			return statement

		else:
		

			parts = statement.split(" ")

			# Isolating time number
			the_time = []
			for el in parts:
				if "AM" in el:
					the_time.append(el[:el.find("AM") + 2].strip())
				if "PM" in el:
					the_time.append(el[:el.find("PM") + 2].strip())


			# Translating into a valid number		
			new_stmt = statement
			for t in the_time:
				new_time_val = "null"

				if "AM" in t:
					new_time_val = t.replace("AM", "")

				if "PM" in t:
					new_time_val = str(int(t.replace("PM", "")) + 12) 

				new_stmt = new_stmt.replace(t,new_time_val)

			return new_stmt


	def correctDay(self, statement):

		if "day" not in statement:
			return statement

		else:
			
			new_stmt = statement
			parts = statement.split(" ")	
			month_indexes = []

			for i in range(0, len(parts)):
				current_el = parts[i].replace(",", "").strip()
				if current_el in self.months_token:
					month_indexes.append(i)


			for i in month_indexes:
				month_str = parts[i].replace(",","").strip()
				day = parts[i+1].replace(")", "").strip()

				month = self.months_token.index(month_str) + 1
				day_number = month * 31 + int(day)
				new_stmt = new_stmt.replace(month_str + ", " + day, str(day_number))

			return new_stmt

	def getRoomAndValFromIntRule(self, rule, token):		

		# The first rule_values cell has to contain the room number
		# All the other values has to contains the intervals limits

		rule_values = []

		#if the rule does not express an interval, i do not have to do anything
		if "=" in rule[0]:
			return rule_values

		if "and" in rule[0]:
			ruleSplit = rule[0].replace(token, "").replace("and","#").replace("(","#").replace(")","#").replace(">","#").replace("<","#").replace(" ", "").strip().split("#")

			for t in ruleSplit:
				if len(t) > 0:
					rule_values.append(t)

			# Removing the duplicate room number
			# The room number has to be first in the list
			rule_values.pop(2)
			room = rule_values[1]
			rule_values[1] = rule_values[0]
			rule_values[0] = room

		else:

			#Finding the room number and the temperature number
			ruleSplit = rule[0].replace(token, "").replace("(","#").replace(")","#").replace(">","#").replace("<","#").replace(" ", "").strip().split("#")
			for t in ruleSplit:
				if len(t) > 0:
					rule_values.append(t)
			

		return rule_values

	def generateIntAssertionList(self, assecrtionDict, room, smt_constant):
		assertions = []

		if len(assecrtionDict[room]) > 0:
			assertions.append(("(< " + smt_constant + " " + str(assecrtionDict[room][0]) + ")").replace(self.__ROOMTAG,room))

			for i in range(1,len(assecrtionDict[room])):
				part0 = "< " + str(assecrtionDict[room][i-1]) + " " + smt_constant 
				part1 = "< " + smt_constant + " " + str(assecrtionDict[room][i])

				assertions.append( ("(and (" + part0 + ") (" + part1 + ") )").replace(self.__ROOMTAG,room) )

			assertions.append( ("(> " + smt_constant + " " + str(assecrtionDict[room][-1]) + ")").replace(self.__ROOMTAG,room) )

			for t in assecrtionDict[room]:
				assertions.append(("(= " + smt_constant + " " + str(assecrtionDict[room][0]) + ")").replace(self.__ROOMTAG,room))

		return assertions

	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))

	def addPrefixToFileName(self, filename):

		from hashlib import md5
		from time import localtime

		return "%s_%s_%s" % (self.id_generator(), md5(str(localtime())).hexdigest(), filename)

	def check(self):

		#filtered_rules = self.filterSpecifiedRulesByLocation("room 234")
		filtered_rules  = self.specified_rules


		translated_rules = []
		for rule in filtered_rules:
			rule[0] = self.antecedentTranslation(rule[0])
			rule[1] = self.consequentTranslation(rule[1])


			# Translating time
			rule[0] = self.correctTime(rule[0])	
			rule[1] = self.correctTime(rule[1])

			# Translating day		
			rule[0] = self.correctDay(rule[0])	
			rule[1] = self.correctDay(rule[1])

			# Replacing tags	
			rule[0] = rule[0].replace(self.__ROOMTAG, rule[2])
			rule[1] = rule[1].replace(self.__ROOMTAG, rule[2])

			# Adding dynamic declaration for sockets
			if self.__POWER_SOCKET_ON in rule[1]:
				fun_name = rule[1].replace("(", "").replace(")", "").replace("not", "").strip()
				new_dec = "declare-fun " + fun_name + " () Bool"
				if new_dec not in self.dynamic_declaration:
					self.dynamic_declaration.append(new_dec)
			
			# Adding room to rooms list
			if rule[2] not in self.rooms_list:
				self.rooms_list.append(rule[2])

			translated_rules.append(rule)


		## Creatint Z3 SMT output file
		output_file_partial = []


		#File Header and Settings
		f = open(self.__MAIN_PATH + "header_template.txt")
		lines = f.readlines()
		f.close()
		for line in lines:
			output_file_partial.append(line[1:-2])


		for dec in self.dynamic_declaration:
			output_file_partial.append(dec)

		#File Body

		ruleCont = 0
		for rule in translated_rules:
			output_file_partial.append("assert (=> " + rule[0] + " " + rule[1] + ")")
			ruleCont += 1

		#Getting antecedents to create assertions
		assertions = []
		temperatureAssertionDict = {}
		timeAssertionDict = {}

		for r in self.rooms_list:
			temperatureAssertionDict[r] = []
			timeAssertionDict[r] = []

		for rule in filtered_rules:
			if rule[0] not in assertions:
				assertions.append(rule[0])


		#Managing integer rules assertions
		for rule in filtered_rules:

			if self.__TEMPERATURE_TOKEN in rule[0]:
				rule_values = self.getRoomAndValFromIntRule(rule, self.__TEMPERATURE_TOKEN)
				if len(rule_values)>0:
					room = rule_values[0]
					for val in rule_values[1:]:
						if int(val) not in temperatureAssertionDict[room]:
							temperatureAssertionDict[room].append(int(val))
							temperatureAssertionDict[room].sort()

			if self.__TIME_TOKEN in rule[0]:
				rule_values = self.getRoomAndValFromIntRule(rule, self.__TIME_TOKEN)
				if len(rule_values)>0:
					room = rule_values[0]
					for val in rule_values[1:]:
						if int(val) not in timeAssertionDict[room]:
							timeAssertionDict[room].append(int(val))
							timeAssertionDict[room].sort()

		for r in self.rooms_list:
			assertions.extend(self.generateIntAssertionList(temperatureAssertionDict, r, self.__TEMPERATURE))
			assertions.extend(self.generateIntAssertionList(timeAssertionDict, r, self.__TIME))

		if len(self.errorList) > 0:
			print "RulesetChecker@@ Some errors occurred! Checking will not be performed!"
			return self.errorList

		print "RulesetChecker@@ Checking..."

		out_file = []
		for check_assertion in assertions:
			out_file = output_file_partial[:]
			out_file.append("assert " + check_assertion)

			#File Bottom
			out_file.append("check-sat")
			#out_file.append("get-model")

			#Generating output file
			the_out_file = ""
			for line in out_file:
				if len(line.strip())>0:
					tmp_str = "(" + line + ")"
				the_out_file += tmp_str + "\n"


			temporary_file_path = self.__MAIN_PATH + self.addPrefixToFileName("test_smt.z3")
			out_file = open(temporary_file_path,"w")
			out_file.write(the_out_file)
			out_file.close()	

			exec_str = self.__MAIN_PATH + "z3/bin/z3 -smt2 " + temporary_file_path
			print exec_str
			z3_output = subprocess.check_output(exec_str, shell=True)
			os.remove(temporary_file_path)
			#print the_out_file
			print z3_output
			#print ""
			#print ""
			#print ""
			#print ""

			
			if "unsat" in z3_output:
				error =  "There is a conflict in the rules!"
				print error
				self.errorList.append(error)
				return self.errorList

			#raw_input("Premi invio...")


		print "There is no conflicts in the rules!"
		return self.errorList

