sol = [[12, 6, 2, 10, 30],
	   [8, 1, 5, 4, 18],
	   [7, 9, 3, 11, 30],
	   [27, 16, 10, 25]]


class SurvoBacktrack:
	def solve(self, puzzle):
		self.lines = len(puzzle) - 1
		self.columns = len(puzzle[0]) - 1
		
		self.start_number = 1
		self.max_number = (self.lines) * (self.columns)
		
		self.ruletable = [[0] * (self.lines)] * 2
		for i in range(self.lines):
			self.ruletable[0][i] = puzzle[i][-1]
			puzzle[i] = puzzle[i][:-1]
		self.ruletable[1] = puzzle[-1]
		puzzle = puzzle[:-1]
		
		if self.solver(puzzle):
			return self.solution
		else:
			return None
	
	def solver(self, puzzle):
		# check if we found the solution, first for the lines and then for the columns
		rules_respected = 0
		for i in range(self.lines):
			line_filled = True
			line_sum = 0
			for j in range(self.columns):
				if not puzzle[i][j]:
					line_filled = False
					break
				else:
					line_sum += puzzle[i][j]
			if line_filled:
				if line_sum != self.ruletable[0][i]:
					return False
				else:
					rules_respected += 1
		
		for j in range(self.columns):
			line_filled = True
			line_sum = 0
			for i in range(self.lines):
				if not puzzle[i][j]:
					line_filled = False
					break
				else:
					line_sum += puzzle[i][j]
			if line_filled:
				if line_sum != self.ruletable[1][j]:
					return False
				else:
					rules_respected += 1
				
		if rules_respected == self.lines + self.columns:
			self.solution = puzzle
			for i in range(self.lines):
				self.solution[i].append(self.ruletable[0][i])
			self.solution.append(self.ruletable[1])
			return True
		
		available_numbers = []
		for number in range(self.start_number, self.max_number + 1):
			number_free = True
			for i in range(self.lines):
				for j in range(self.columns):
					if number == puzzle[i][j]:
						number_free = False
						break
			if number_free:
				max_available_number = number
				available_numbers.append(number)
		
		# start with the most constrained variables
		for i in range(self.lines):
			for j in range(self.columns):
				if not puzzle[i][j]:
					for number in available_numbers:
						# we know there is at least one 0 (the one we are considering to replace)
						count = 0
						count_0 = -1
						for l in range(self.columns):
							if not puzzle[i][l]:
								count_0 += 1
							else:
								count += puzzle[i][l]
						# this is but an approximation, we do not cut all non possible solutions this way
						# notably, one could check for the maximum number possible as well
						if count + number + count_0 * max_available_number < self.ruletable[0][i]:
							continue
						
						count = 0
						count_0 = -1
						for k in range(self.lines):
							if not puzzle[k][j]:
								count_0 += 1
							else:
								count += puzzle[k][j]
						if count + number + count_0 * max_available_number < self.ruletable[1][j]:
							continue
						
						puzzle[i][j] = number
						if self.solver(puzzle):
							return True
						puzzle[i][j] = 0


if __name__ == "__main__":
	puzzle = [[0, 6, 0, 0, 30],
			  [8, 0, 0, 0, 18],
			  [0, 0, 3, 0, 30],
			  [27, 16, 10, 25]]
	solver = SurvoBacktrack()
	print(solver.solve(puzzle))
