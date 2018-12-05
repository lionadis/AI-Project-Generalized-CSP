from CSP import CSP
from CSP_Solver import CSP_Solver

def initialzing_NQueen(N):

	csp = CSP()
	def rule(X, x, Y, y):
		if x[0] == y[0]: return False
		if x[1] == y[1]: return False
		if abs((x[0] - y[0]) / (x[1] - y[1])) == 1: return False
		return True
	
	for v in range(N):
		csp.add_variable(v, [(x, y) for x in range(N) for y in range(N)])
	csp.domains[0] = [(1, 0)]			
	for x in csp.variables:
		for y in csp.variables:
			if x != y:
				csp.add_constraint(x, y, rule)
	return csp

N = 4

def print_solution(assignment):

	if assignment == None:
		print("No Solution!!!")
		return
	board = [['.'] * N for i in range(N)]
	for i in range(N):
		x = assignment[i][0][0]
		y = assignment[i][0][1]
		assert(board[x][y] == '.')
		board[x][y] = 'Q'
	for i in range(N):
		print(board[i])


def main():

	nqueen = initialzing_NQueen(N)
	csp_solver = CSP_Solver(nqueen)
	print(csp_solver.solve())
	print_solution(csp_solver.backtrack_search())
	print(csp_solver.calls)
if __name__ == "__main__":
	main()

