from z3 import *

def is_black(case):
	return case >= 0 and case <= 4

def LightSat(puzzle):
	s = Solver()
	
	lines = len(puzzle)
	columns = len(puzzle[0])
	
	# create the solver matrix
	X = [ [ Int("b%d%d" % (i, j)) if not is_black(puzzle[i][j]) else puzzle[i][j] for j in range(columns) ]
		  for i in range(lines) ]
	
	# input the given values, or give the possibilities
	for i in range(lines):
		for j in range(columns):
			# -1 is for a light, 0 for nothing
			if(not is_black(puzzle[i][j])):
				s.add(X[i][j] < 1)
				s.add(X[i][j] > -2)
	
	# lights cannot be adjacent
	for i in range(lines):
		for j in range(columns):
			if(i > 0):
				s.add(Implies(X[i][j] == -1, X[i-1][j] != -1))
			if(j > 0):
				s.add(Implies(X[i][j] == -1, X[i][j-1] != -1))
			if(i < lines-1):
				s.add(Implies(X[i][j] == -1, X[i+1][j] != -1))
			if(j < columns-1):
				s.add(Implies(X[i][j] == -1, X[i][j+1] != -1))
	
	# when there is a light it lights up everything in 4 directions (-1 of everything)
	for i in range(lines):
		for j in range(columns):
			if(is_black(puzzle[i][j])):
				s.add( sum(X[m][j] for m in range(i + 1, lines) if not is_black(puzzle[m][j])) + sum(X[m][j] for m in range(i) if not is_black(puzzle[m][j])) + sum(X[i][k] for k in range(j + 1, columns) if not is_black(puzzle[i][k])) + sum(X[i][k] for k in range(j) if not is_black(puzzle[i][k])) == -X[i][j] )

	if s.check() == sat:
		boarde = str(s.model())
		for i in range(lines):
			for j in range(columns):
				if(puzzle[i][j] < 0):
					x = boarde.find(str("b" + str(i) + str(j)))
					puzzle[i][j] = int(boarde[x+6:boarde.find(",", x+6)]) - 1
					if puzzle[i][j] == -2:
						puzzle[i][j] = "!"
		return puzzle
	else:
		return "Cannot Solve"
	
if __name__ == "__main__":
	# puzzle encoding: numbers between 0 and 4 represent the black cells, otherwise a negative number means an empty cell that could be a light
	puzzle = [[-1, 0, -1],
			  [-1, 2, -1]]
	print(LightSat(puzzle))
