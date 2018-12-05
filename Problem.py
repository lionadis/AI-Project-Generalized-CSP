from CSP import CSP

class Problem:

	def __init__(self):
		self.variables = []
		self.domains = []
		self.neighbors = []
		self.constraints = []


class NQueen(Problem):
	def __init__(self, N):
		self.N = N
		self.variables =  list(range(N))
		self.domains = [list(range(N * N)) for i in range(N)]
		self.neighbors = [list(range(N)) for i in range(N)]
		for i in range(N):
			self.neighbors[i].remove(i)

	def constraints(self, X, x, Y, y):
		xi = x // self.N
		xj = x % self.N
		yi = y // self.N
		yj = y % self.N
		
		if xi == yi : return False #Same row
		if xj == yj : return False #Same column
		if abs((xi - yi) / (xj - yj)) == 1: return False #same diagonal
		return True

	def print_solution(self, assignment):
		if assignment == None:
			print("No Solution!!!")
			return
		board = [['.'] * self.N for i in range(self.N)]
		for i in range(self.N):
			x = assignment[i][0] // self.N
			y = assignment[i][0] % self.N
			assert(board[x][y] == '.')
			board[x][y] = 'Q'
		for i in range(self.N):
			print(board[i])

def main():
	nq = NQueen(7)
	csp = CSP(nq, ac3=True)
	csp.AC3()
	nq.print_solution(csp.backtrack_search())
	print(csp.calls)
if __name__ == "__main__":
	main()

