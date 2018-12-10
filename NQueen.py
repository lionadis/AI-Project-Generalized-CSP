from CSP import CSP

def initialzing_NQueen(N):

	csp = CSP()
	
	rule = "x[0] != y[0] and x[1] != y[1] and abs((x[0] - y[0]) / (x[1] - y[1])) != 1"

	for v in range(N):
		csp.add_variable(str(v), [[x, y] for x in range(N) for y in range(N)])

	for x in csp.variables:
		for y in csp.variables:
			if x != y:
				csp.add_constraint(x, y, rule)
	csp.solve()
	csp.save_solution()
#	print(csp.solutions)
	return csp

N = 5 

def print_solution(assignment):

	if assignment == None:
		print("No Solution!!!")
		return
	print(assignment)
	board = [['.'] * N for i in range(N)]
	for i in range(N):
		x = assignment[str(i)][0][0]
		y = assignment[str(i)][0][1]
		assert(board[x][y] == '.')
		board[x][y] = 'Q'
	for i in range(N):
		print(board[i])


def main():

	nqueen = initialzing_NQueen(N)
	nqueen.export_to_json("nqueen.json")
if __name__ == "__main__":
	main()

