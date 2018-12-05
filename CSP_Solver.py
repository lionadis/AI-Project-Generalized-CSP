from copy import deepcopy
from random import choice
from functools import cmp_to_key

class CSP_Solver: 

	def __init__(self, problem, ac3=True, heuristic="mrv", lcs=True):

		self.calls = 0
		self.problem = problem
		self.ac3 = ac3
		self.heuristic=heuristic
		self.lcs = lcs
		self.cleared_values = 0

	def is_complete(self):

		return all([len(self.problem.domains[X]) == 1 for X in self.problem.variables])

	def check_consistency(self, X, x):
		
		for Y, rule in self.problem.neighbors[X].items():
			if len(self.problem.domains[Y]) == 1 and not rule(X, x, Y, self.problem.domains[Y][0]):
#print("Error assiging %s to %s since %s is assigned to %s"%(X, x, Y, self.problem.domains[Y][0]))
				return False
#		print("Assiging %s to %s"%(X, x))
		return True

	def get_unassigned_variables(self, X = None):
		
		if X is None:
			return [x for x in self.problem.variables if len(self.problem.domains[x]) > 1]
		else:
			return [x for x, rule in self.problem.neighbors[X].items() if len(self.problem.domains[x]) > 1]

	def choose_unassigned_variable_FIRST(self):

		return self.get_unassigned_variables()[0]

	def choose_unassigned_variable_RANDOM(self):

		return choice(self.get_unassigned_variables())

	def choose_unassigned_variable_MRV(self):

		def compare(X, Y):
			return len(self.problem.domains[X]) < len(self.problem.domains[Y])

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

			return sum([not rule(X, x1, Y, y) for Y, rule in self.problem.neighbors[X].items() for y in self.problem.domains[Y]]) \
				<  sum([not rule(X, x2, Y, y) for Y, rule in self.problem.neighbors[X].items() for y in self.problem.domains[Y]])
	
		return sorted(self.problem.domains[X], key = cmp_to_key(compare))

	def AC3(self, X = None):
		
		if X is None:
			Q = [(x, y) for x in self.problem.variables for y in self.problem.neighbors[x]]
		else:
			Q = [(X, Y) for Y in self.get_unassigned_variables(X)]
		print(Q)
		while len(Q):
			(X, Y) = Q.pop()
			if self.clear_inconsistent_values(X, Y):
				if len(self.problem.domains[X]) == 0:
					 return False
				for Z in self.problem.neighbors[X]:
					if Z != Y:
						Q.append((Z, X))
		print("Values cleared by AC3 %s"%(self.cleared_values))
		self.cleared_values = 0
		return True

	def clear_inconsistent_values(self, X, Y):

		modified = False
		for x in self.problem.domains[X]:
			if not any([self.problem.neighbors[X][Y](X, x, Y, y) and self.problem.neighbors[Y][X](X, x, Y, y) for y in self.problem.domains[Y]]):
				self.cleared_values += 1
				self.problem.domains[X].remove(x)
				print(X, x)
				modified = True
		return modified
	

	def get_domain_ordering(self, X):

		if self.lcs == True:
			return self.order_by_least_constraining_value(X)
		else:
			return self.problem.domains[0]

	def backtrack_search(self):
		self.calls += 1
		if self.is_complete():
			return self.problem.domains
		
		X = self.choose_next_unassigned_variable()

		for x in self.get_domain_ordering(X):
			if self.check_consistency(X, x):
				current_domains = deepcopy(self.problem.domains)
				self.problem.domains[X] = [x]
				mac = False
				if self.ac3 == True:
					mac = self.AC3(X)
				if mac or self.ac3 == False:
					result = self.backtrack_search()
				if result != None:
					return result
				self.problem.domains = current_domains
		return None

	def solve(self):
		if self.ac3:
			self.AC3()
			print("STARTING BACKTRACK")
			return self.backtrack_search()
		else:
			return self.backtrack_search()

