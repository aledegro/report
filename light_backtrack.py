class LightBacktrack:
	def solve(self, puzzle):
		self.lines = len(puzzle[0]) - 1
		self.columns = len(puzzle)
		self.puzzle = puzzle
		
		
		if self.solver():
			return self.solution
		else:
			return "Cannot solve"
	
	def solver(self):
		found = True
		for i in range(self.lines):
			for j in range(self.columns):
				if(self.puzzle[i][j] != "!" and self.puzzle[i][j] >= 0 and self.lighted(i, j) != 0):
					found = False
					break
		if(found):
			self.solution = self.puzzle
			return True
		
		for i in range(self.lines):
			for j in range(self.columns + 1):
				if self.puzzle[i][j] != "!" and self.puzzle[i][j] < 0 and self.can_place_light(i, j):
					self.puzzle[i][j] = "!"
					if self.solver():
						return True
					self.puzzle[i][j] = -1
	
	def lighted(self, i, j):
		amount = self.puzzle[i][j]
		for k in range(1, j + 1):
			if self.puzzle[i][j-k] == "!":
				amount -= 1
				break
			elif self.puzzle[i][j-k] >= 0:
				break
		for k in range(1, self.columns - j + 1):
			if self.puzzle[i][j+k] == "!":
				amount -= 1
				break
			elif self.puzzle[i][j+k] >= 0:
				break
		for l in range(1, i + 1):
			if self.puzzle[i-l][j] == "!":
				amount -= 1
				break
			elif self.puzzle[i-l][j] >= 0:
				break
		for l in range(1, self.lines - i):
			if self.puzzle[i+l][j] == "!":
				amount -= 1
				break
			elif self.puzzle[i+l][j] >= 0:
				break
		return amount
	
	def can_place_light(self, i, j):
		for k in range(1, j + 1):
			if self.puzzle[i][j-k] == "!" or self.puzzle[i][j-k] == 0:
				return False
			elif self.puzzle[i][j-k] >= 0:
				break
		for k in range(1, self.columns + 1 - j):
			if self.puzzle[i][j+k] == "!" or self.puzzle[i][j+k] == 0:
				return False
			elif self.puzzle[i][j+k] >= 0:
				break
		for l in range(1, i + 1):
			if self.puzzle[i-l][j] == "!" or self.puzzle[i-l][j] == 0:
				return False
			elif self.puzzle[i-l][j] >= 0:
				break
		for l in range(1, self.lines - i):
			if self.puzzle[i+l][j] == "!" or self.puzzle[i+l][j] == 0:
				return False
			elif self.puzzle[i+l][j] >= 0:
				break
		return True
				
				

if __name__ == "__main__":
	puzzle = [[-1, 0, -1],
			  [-1, 2, -1]]
	solver = LightBacktrack()
	print(solver.solve(puzzle))
