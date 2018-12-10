def main():
	import tkinter
	import time
	import sys
	sys.path.append("./chess_tkinter/")
	from chess_tkinter.ChessBoard import ChessBoard
	import json
	from random import choice
	solution = choice(json.load(open("solutions.json", "r")))
	# root window
	root = tkinter.Tk()
	root.wm_title("Chess Board")
	N = len(solution)
	# reserve board on root
	cb = ChessBoard(root, N=N)
	h = "87654231"
	w = "abcdefgh"
	for key, value in solution.items():
		cb.canvas.update_idletasks()
		cb.placePiece(w[value[0][0]] + h[value[0][1]], "Q")
	cb.pack()
	# run
	root.mainloop()


if __name__ == "__main__":

	main()
