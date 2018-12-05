from CSP_Solver import CSP_Solver

class CSP():

	def __init__(self):
		self.variables = []
		self.domains = dict()
		self.neighbors = dict()
	
	def add_variable(self, var, domain):
		self.variables.append(var)
		self.domains[var] = domain
		self.neighbors[var] = dict()
	
	def add_constraint(self, x, y, rule):
		self.neighbors[x][y] = rule



