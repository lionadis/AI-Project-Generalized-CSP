from copy import deepcopy
from random import choice
from functools import cmp_to_key
from inspect import getsourcelines
import json

class Constraint():

	def __init__(self, rule):
		self.rule = rule
		self.f = lambda x, y : eval(rule)


class CSP: 

	def __init__(self, ac3=True, heuristic="mrv", lcs=True, all_solutions = True):

		# Defining CSP
		self.variables = []
		self.domains = dict()
		self.neighbors = dict()
	
		# Choosing heuristics
		self.ac3 = ac3
		self.heuristic = heuristic.lower()
		self.lcs = lcs

		self.all_solutions = all_solutions
		self.solutions = []
		self.calls = 0
		self.cleared_values = 0

	def add_variable(self, var, domain):
		self.variables.append(var)
		self.domains[var] = domain
	
	def add_constraint(self, x, y, rule):

		try:
			self.neighbors[x][y] = Constraint(rule)
		except:
			self.neighbors[x] = dict()
			self.neighbors[x][y] = Constraint(rule)

			self.neighbors[y] = dict()

	def is_complete(self):
		return all([len(self.domains[X]) == 1 for X in self.variables])

	def check_consistency(self, X, x):
		
		for Y, rule in self.neighbors[X].items():
			if len(self.domains[Y]) == 1 and not rule.f(x, self.domains[Y][0]):
				print("Error assiging %s to %s since %s is assigned to %s"%(X, x, Y, self.domains[Y][0]))
				return False
		print("Assiging %s to %s"%(X, x))
		return True

	def get_unassigned_variables(self, X = None):
		
		if X is None:
			return [x for x in self.variables if len(self.domains[x]) > 1]
		else:
			return [x for x, rule in self.neighbors[X].items() if len(self.domains[x]) > 1]

	def choose_unassigned_variable_FIRST(self):

		return self.get_unassigned_variables()[0]

	def choose_unassigned_variable_RANDOM(self):

		return choice(self.get_unassigned_variables())

	def choose_unassigned_variable_MRV(self):

		def compare(X, Y):
			return len(self.domains[X]) < len(self.domains[Y])
		return sorted(self.get_unassigned_variables(), key = cmp_to_key(compare))[0]

	def choose_unassigned_variable_DH(self):

		def compare(X, Y):
			return len(self.get_unassigned_variables(X)) > len(self.get_unassigned_variables(Y))

		return sorted(self.get_unassigned_variables(), key = cmp_to_key(compare))[0]

	def choose_next_unassigned_variable(self):

		if self.heuristic == "mrv":
			return self.choose_unassigned_variable_MRV()
		elif self.heuristic == "dh":
			return self.choose_unassigned_variable_DH()
		elif self.heuristic == "first":
			return self.choose_unassigned_variable_FIRST()
		else:
			return self.choose_unassigned_variable_RANDOM()

	
	def order_by_least_constraining_value(self, X):

		def compare(x1, x2):	

			return sum([not rule.f(x1, y) for Y, rule in self.neighbors[X].items() for y in self.domains[Y]]) \
				<  sum([not rule.f(x2, y) for Y, rule in self.neighbors[X].items() for y in self.domains[Y]])
	
		return sorted(self.domains[X], key = cmp_to_key(compare))

	def AC3(self, X = None):
		
		if X is None:
			Q = [(x, y) for x in self.variables for y in self.neighbors[x]]
		else:
			Q = [(X, Y) for Y in self.get_unassigned_variables(X)]
		while len(Q):

			(X, Y) = Q.pop()
			if self.clear_inconsistent_values(X, Y):
				if len(self.domains[X]) == 0:
					 return False
				for Z in self.neighbors[X]:
					if Z != Y:
						Q.append((Z, X))
		print("Values cleared by AC3 %s"%(self.cleared_values))
		self.cleared_values = 0
		return True

	def clear_inconsistent_values(self, X, Y):

		modified = False
		for x in self.domains[X]:
			if not any([self.neighbors[X][Y].f(x, y) for y in self.domains[Y]]):
				self.cleared_values += 1
				self.domains[X].remove(x)
				modified = True
		return modified
	

	def get_domain_ordering(self, X):

		if self.lcs == True:
			return self.order_by_least_constraining_value(X)
		else:
			return self.domains[X]

	def backtrack_search(self):

		self.calls += 1

		if self.is_complete():
			self.solutions.append(self.domains)
			print(self.domains)
			if not self.all_solutions:
				return True
			else:
				return None
		X = self.choose_next_unassigned_variable()

		for x in self.get_domain_ordering(X):
			if self.check_consistency(X, x):
				current_domains = deepcopy(self.domains)
				self.domains[X] = [x]
				mac = False
				if self.ac3 == True:
					mac = self.AC3(X)
				if mac or self.ac3 == False:
					result = self.backtrack_search()
				if result != None:
					return result
				self.domains = current_domains

		return None

	def solve(self):

		if self.ac3:
			self.AC3()
		self.backtrack_search()
		if self.all_solutions:
			return self.solutions
		else:
			if len(self.solutions) >= 1:
				return self.solutions[0]
			else :
				return 0

	def load_from_json(self, filename):

		problem = json.load(open(filename, 'r'))
	
		self.__init__()

		for var, domain in problem['domains'].items():
			self.add_variable(var, domain)

		for constraint in problem['constraints']:
			self.add_constraint(constraint['scope'][0], constraint['scope'][1], constraint['rule'])


	def export_to_json(self, filename):

		problem = dict()
		problem["domains"] = self.domains
		problem["constraints"] = []
		for x, value in self.neighbors.items():
			for y, rule in value.items():
				constraint = dict()
				constraint["scope"] = [x, y]
				constraint["rule"] = rule.rule
				problem["constraints"].append(constraint)
		json_file = open(filename, "w")
		json_file.write(json.dumps(problem))
	
