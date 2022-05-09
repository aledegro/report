from z3 import *
import matplotlib.pyplot as plt
import os
import time

def SurvoSat(puzzle):
	# Note: We assume the given puzzle corresponds to the rules.
	start_number = 1
	lines = len(puzzle) - 1
	columns = len(puzzle[0]) - 1
	max_number = (lines) * (columns)

	s = Solver()

	# Create a matrix of integer variables.
	X = [ [ Int("b%d%d" % (i, j)) if (puzzle[i][j] == 0) else puzzle[i][j] for j in range(columns) ]
		  for i in range(lines) ]

	# The numbers within the matrix are all contained within start_number and max_number.
	for i in range(lines):
		for j in range(columns):
			if(puzzle[i][j] == 0):
				s.add(And(start_number <= X[i][j], X[i][j] <= max_number))

	# The numbers within the matrix are all distinct.
	s.add(Distinct([X[i][j] for i in range(lines) for j in range(columns)]))

	# The sum of the numbers in a row/column most be equal to the end of the row/column.
	for i in range(lines):
		s.add(Sum(X[i][:]) == puzzle[i][-1])
	for j in range(columns):
		s.add(Sum([X[i][j] for i in range(lines)]) == puzzle[-1][j])

	if s.check():
		boarde = str(s.model())
		for i in range(lines):
			for j in range(columns):
				if(puzzle[i][j] == 0):
					x = boarde.find(str("b" + str(i) + str(j)))
					puzzle[i][j] = int(boarde[x+6:boarde.find(",", x+6)])
		return puzzle
	else:
		return None



if __name__ == "__main__":
	puzzle = [[0, 6, 0, 0, 30],
			  [8, 0, 0, 0, 18],
			  [0, 0, 3, 0, 30],
			  [27, 16, 10, 25]]
	SurvoSat(puzzle)
