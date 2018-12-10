from CSP import CSP

def initialize_sudoku():

	csp = CSP()
	N = 4
	BLOCK = 2
	rule = "x != y" 

	for i in range(N):
		for j in range(N):
			csp.add_variable("(%s, %s)"%(i, j), list(range(N)))
	
	for x1 in range(N):
		for y1 in range(N):
			for x2 in range(N):
				for y2 in range(N):
					neighbors = False
					if x1 == x2: neighbors = True
					if y1 == y2: neighbors = True
					if x1 // BLOCK == x2 // BLOCK and y1 // BLOCK == y2 // BLOCK: neighbors = True
					if neighbors:
						csp.add_constraint("(%s, %s)"%(x1, y1), "(%s, %s)"%(x2, y2), rule)

	csp.export_to_json("sudoku.json")
	csp.all_solutions = False
	solution = csp.solve()
	board = [[0] * N for i in range(N)]
	print(len(board))
	for key, value in solution.items():
		print(key[1], key[4], value)
		board[int(key[1])][int(key[4])] = value[0]

	for i in range(N):
		print(board[i])
	

if __name__ == "__main__":

	initialize_sudoku()
