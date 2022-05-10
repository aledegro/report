from os.path import exists

with open('puzzles.txt', 'r', encoding="utf-8") as f:
	lines = f.readlines()
	filling = False
	board = [[]]
	for x in range(len(lines)):
		line = lines[x].strip();
		if(line[-2:] == "},"):
			number = 0
			while exists(str(width) + "x" + str(height) + "#" + str(number) + ".survo"):
				number += 1
			fil = open(str(width) + "x" + str(height) + "#" + str(number) + ".survo", 'x')
			# removes the empty element at the end
			board = board[:-1]
			# all elements except the rules to 0
			#for i in range(len(board)):
			#	for j in range(len(board[i])):
			#		if(i != len(board) and j != len(board[0]):
			#			board[i][j] = "0,"
			fil.write(board)
			fil.close()
			filling = False
		elif(line[:7] == '"name":'):
			name = line[8:]
		elif(line[:8] == '"board":'):
			board = [[]]
			width = 0
			height = 0
			filling = True
		elif(filling and line[-1] != "[" and line[-1] != "]" and line[-2:] != "],"):
			board[height].append(line)
			if(height == 0):
				width += 1
			if(line[-1] != ","):
				board = board + "\n"
				height += 1