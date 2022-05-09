from survo_sat import *
from survo_backtrack import *
from copy import deepcopy
import matplotlib.pyplot as plt
import os
import time
TRIES = 1 # how many times you want to test each puzzle 
MODE = "BACKTRACK" # or "SAT"

def findTime():
	results = open("results" + MODE + ".txt", 'w')
	plt.ylabel("Time needed")
	plt.xlabel("Size of the grid")
	plt.title("Speed of SMT solver for different survo sizes")
	resultX = []
	resultY = []
	if(MODE == "BACKTRACK"):
		backtracker = SurvoBacktrack()

	for filename in os.listdir('survos'):
		# Don't want to spend my life waiting.
		if(MODE == "BACKTRACK" and int(filename[filename.find("#") + 1 : filename.find(".")]) > 5):
			continue
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
		for i in range(TRIES):
			puzzle = deepcopy(board)
			if(MODE == "SAT"):
				SurvoSat(puzzle)
			elif(MODE == "BACKTRACK"):
				backtracker.solve(puzzle)
		totalTime = time.time() - startTime
		resultX.append(totalTime / TRIES)
		resultY.append(filename[:filename.find("#")])
		resultY[-1] = int(resultY[-1][:resultY[-1].find("x")]) * int(resultY[-1][resultY[-1].find("x")+1:])
		results.write(str(totalTime) + " for " + filename + "\n")
	results.close()
	yType = []
	for types in resultY:
		if types not in yType:
			yType.append(types)
	
	averageX = [0] * len(yType)
	precision = [0] * len(yType)
	for x in range(len(resultX)):
		position = yType.index(resultY[x])
		averageX[position] += resultX[x]
		precision[position] += 1
	for x in range(len(averageX)):
		averageX[x] = averageX[x] / precision[x]
	print(precision, averageX)
	
	if(MODE == "SAT"):
		coloring = 'b'
	else:
		coloring = 'r'
	plt.scatter(yType, averageX, color=coloring)
	plt.show()
	
if __name__ == "__main__":
	findTime()