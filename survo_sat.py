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
	results = open("results.txt", 'w')
	plt.xlabel("Time needed")
	plt.ylabel("Size of the grid")
	plt.title("Speed of SMT solver for different survo sizes")
	resultX = []
	resultY = []

	for filename in os.listdir('survos'):
		board = []
		with open("survos/" + filename, 'r') as file:
			lines = file.readlines()
			for line in lines:
				firstComa = -1
				row = []
				for i in range(len(line)):
					if line[i] == ',':
						row.append(int(line[firstComa+1: i]))
						firstComa = i
				row.append(int(line[firstComa+1: len(line)]))
				board.append(row)
		startTime = time.time()
		SurvoSat(board)
		totalTime = time.time() - startTime
		resultX.append(totalTime)
		resultY.append(filename[:filename.find("#")])
		results.write(str(totalTime) + " for " + filename)
	results.close()
	averageX = [0]
	averageY = [0]
	precision = []
	type = resultY[0]
	print(type)
	number = 0
	for x in range(len(resultX)):
		if(resultY[x] != type):
			averageX[-1] /= number
			averageX.append(0)
			averageY[-1] /= number
			averageY.append(0)
			precision.append(number)
			number = 0
		averageX[-1] += resultX[x]
		averageY[-1] += resultY[x]
		number += 1

	sortedPrecision = precision.sort()
	colors = ["c", "b", "y", "g", "m", "r", "k"]
	for x in range(len(averageX)):
		plot.plot(averageX[x], averageY[x], color=colors[sortedPrecision.find(precision[x])])
	plt.show()