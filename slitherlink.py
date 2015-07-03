
# For convenience

X = None



class SlitherlinkPuzzle(object):
	"""docstring for SlitherlinkPuzzle"""

	def __init__(self, arg):
		""" This method initializes the puzzle, which is internally 
		represented as a list of lists that contains as elements the values 
		in each of the squares of the puzzle."""

		# We store the list of lists in self.board, the first argument
		self.board = arg

		# self.rows and self.cols represent the number of rows and columns on 
		# the board
		self.rows = len(arg)
		self.cols = len(arg[0])

		# Check each row has the same length
		for i in range(self.rows):
			assert len(arg[i]) == self.cols

		# Check that each element of the array is 0,1,2,3,4 or empty 
		# (represented by the None value)
		for i in range(self.rows):
			for j in range(self.cols):
				assert arg[i][j] in [X,0,1,2,3,4]


		# We now create a field which contains a list of all possible line 
		# segments between vertices of the puzzle. These are represented as a 
		# tuple of pairs representing the coordinates of the vertices, with 
		# the upper left first.

		self.list_of_lines = []

		# First the horizontal list_of_lines
		for i in range(self.rows+1):
			for j in range(self.cols):
				self.list_of_lines.append(((i,j),(i,j+1)))
		# Then the vertical
		for i in range(self.rows):
			for j in range(self.cols+1):
				self.list_of_lines.append(((i,j),(i+1,j)))

		self.list_of_lines = sorted(self.list_of_lines)

		# We now put these in set form, for quick membership tests

		self.set_of_lines = set(self.list_of_lines)


		# We now create lists and sets for vertices and squares

		self.vertices = [(i, j) for i in range(self.rows+1) for j in range(self.cols+1)]
		self.set_of_vertices = set(self.vertices)

		self.squares = [(i, j) for i in range(self.rows) for j in range(self.cols)]
		self.set_of_squares = set(self.squares)



	def prettyprint(self, solution):
		""" A pretty printer for displaying a puzzle instance, along with a 
		partial solution. Partial solutions are represented as dicts that map 
		from lines to booleans. A line is in the dict only if it has been 
		determined, in which case it maps to True, or False corresponding to 
		whether or not the line is in the solution."""

		symbols_array = [[""] * (2*self.cols+1) for i in range (2*self.rows+1)]

		# We populate the symbols array for each vertex, line, and square. 
		# Each vertex and verticle line is a single character, each box and 
		# horizontal line 3 characters
		for i in range(2*self.rows+1):
			for j in range(2*self.cols+1):
				if i % 2 == 0:
					if j % 2 == 0:
						# In this case, we print a vertex
						symbols_array[i][j] = "+"
					else:
						# In this case, we print the solution value for a 
						# horizontal line
						if not ((i/2, j/2), (i/2, j/2 + 1)) in solution:
							symbols_array[i][j] = " . "
						elif solution[((i/2, j/2), (i/2, j/2 + 1))]:
							symbols_array[i][j] = "---"
						else:
							symbols_array[i][j] = "   "
				else:
					if j % 2 == 0:
						# In this case, we print the solution value for a 
						# vertical line					
						if not ((i/2, j/2), (i/2+ 1, j/2 )) in solution:
							symbols_array[i][j] = "."
						elif solution[((i/2, j/2), (i/2+ 1, j/2 ))]:
							symbols_array[i][j] = "|"
						else:
							symbols_array[i][j] = " "
					else:
						# In this case, we print the puzzle value for the
						# square
						if not self.board[i/2][j/2] == None:
							symbols_array[i][j] = " " + str(self.board[i/2][j/2]) + " "
						else:
							symbols_array[i][j] = "   "


				symbols_array[i][j]
			
		# For each row create a new line, populate it, and print it
		for i in range(2*self.rows+1):
			newline = ""
			for j in range(2*self.cols+1):
				newline += symbols_array[i][j]
			print newline

		# Newlines to distinguish boards printed one after the other
		print
		print
		


	
	def print_all_solutions(self):
		""" This method evaluates, then prints out all possible solutions """
		
		print "Evaluating all solutions...\n"
		for solution in self.list_solve():
			assert not self.violation(solution)
			self.prettyprint(solution)
		print "All solutions printed."



	def list_solve(self):
		""" This method computes a list of solutions to the given puzzle, and 
		returns it"""

		# We use an iterative algorithm:
		# We a list containing solutions we have found. We also maintain a 
		# list of partial (not having values for each line) solutions which 
		# have no contradictions, and from the completion of which every 
		# remaining solution can be obtained.


		# Partial solutions initially are just the empty solution
		partial_solutions = [{}]
		solutions = []

		# We iterate until we have exhausted the partial solutions
		while partial_solutions:

			# Retrieve a partial solution to work with. Our idea is to find 
			# an undetermined line, and copy the solution twice, in the two 
			# copies respectively determining the undetermined line as empty 
			# or filled. This creates two new partial solutions, that between 
			# them cover all extensions of the original partial solution. We 
			# then add these back to the partial solution stack, conditional 
			# on them not introducing contradictions to the board.
			partial_solution = partial_solutions.pop()


			# Find, if possible, an empty line
			next_line = None
			for line in self.list_of_lines:
				if line not in partial_solution:
					next_line = line
					break

			# Test to see if the given partial solution is full.
			if next_line == None:
				# The given partial solution is full.
				# Since each line added was tested for violations, this is 
				# valid. Place in solutions and continue
				solutions.append(partial_solution)
				continue

			# At this point, we know that the solution is not full, and line 
			# is currently empty

			# We copy partial solution into two new partial solutions, and 
			# put them in the list
			partial_solution_fill = dict(partial_solution)
			partial_solution_fill[next_line] = True
			if not self.line_violation(partial_solution_fill, next_line):
				partial_solutions.append(partial_solution_fill)

			partial_solution_empty = dict(partial_solution)
			partial_solution_empty[next_line] = False
			if not self.line_violation(partial_solution_empty, next_line):
				partial_solutions.append(partial_solution_empty)

		return solutions

	

	def violation(self, partial_solution):
		""" This method, given a partial solution, checks if the partial 
		solution directly breaks any rules. """

		# Test intersections for no dead ends or forks
		for vertex in self.vertices:
			if self.vertex_violation(partial_solution, vertex):
				return True

		# Test squares for right number of lines
		for square in self.squares:
			if self.square_violation(partial_solution, square):

				return True

		# Test for no two cycles
		# TODO

		# If no violations are found return False
		return False


	def line_violation(self, partial_solution, line):
		""" This method, given a partial solution and a line, checks if the 
		determination of that line breaks any rules. """

		# The given line should make sense
		assert line in partial_solution

		# Unpack the vertices from the line
		vertex0 = line[0]
		i0, j0 = vertex0

		vertex1 = line[1]
		i1, j1 = vertex1

		# Double-check the existence of the vertices
		assert vertex0 in self.set_of_vertices
		assert vertex1 in self.set_of_vertices

		# Test the vertices for violations
		if self.vertex_violation(partial_solution, vertex0):
			return True
		if self.vertex_violation(partial_solution, vertex1):
			return True

		# Test the squares
		square0 = vertex0
		if square0 in self.set_of_squares:
			if self.square_violation(partial_solution, square0):
				return True

		if j1 > j0:
			square1 = (i0-1, j0)
		else:
			square1 = (i0, j0-1)

		if square1 in self.set_of_squares:
			if self.square_violation(partial_solution, square1):
				return True

		# Todo: test against multiple cycles

		return False


	def vertex_violation(self, partial_solution, vertex):
		""" This method, given a partial solution and a vertex, checks if the 
		rule against no branchings or dead ends has been violated for that 
		vertex. """
		
		# Unpack vertex
		i, j = vertex

		# Count the edges from this vertex which are filled, empty and 
		# undetermined
		filled = 0
		empty = 0
		undetermined = 0

		for line in [((i,j),(i,j+1)),
		             ((i,j),(i+1,j)),
		             ((i,j-1),(i,j)),
		             ((i-1,j),(i,j))]:
			if line not in self.set_of_lines:
				pass
			elif not line in partial_solution:
				undetermined += 1
			elif partial_solution[line]:
				filled += 1
			else:
				empty += 1

		# If more than two are filled, this is an illegal branch.
		if filled > 2:
			return True
		# If none are undetermined and there is one filled, this is a dead end.
		if undetermined == 0 and filled == 1:
			return True

		# No contradiction found
		return False


	def square_violation(self, partial_solution, square):
		""" This method, given a partial solution and a square, checks if the 
		rule for number of lines around that square has been broken. """

		# Unpack the square
		i, j = square

		# Check the square makes sense
		assert square in self.set_of_squares

		# If the square is empty, there is no rule to break.
		if self.board[i][j] == None:
			return False

		# Count the edges adjacent to this square which are filled, empty and 
		# undetermined
		filled = 0
		empty = 0
		undetermined = 0

		for line in [((i,j),(i,j+1)),
			         ((i,j),(i+1,j)),
				     ((i,j+1),(i+1,j+1)),
				     ((i+1,j),(i+1,j+1))]:
			if not line in partial_solution:
				undetermined += 1
			elif partial_solution[line]:
				filled += 1
			else:
				empty += 1

		# In this case, even filling all undetermined edges, we have not 
		# enough filled lines
		if self.board[i][j] > filled + undetermined: 
			return True
		# In this case, even emptying all undetermined edges, we have too 
		# many enough filled lines		
		if self.board[i][j] < filled:
			return True

		# No contradiction found
		return False


def retrive_from_file(filename):
	""" Given a filename, parses the file to return a slitherlink instance """
	file = open(filename, "r")
	for line in file:
		print line


if __name__ == "__main__":



	puzzle = \
		SlitherlinkPuzzle(
			[[3,2,2,2,X,X,X],
          	 [2,2,X,3,X,3,2],
          	 [X,X,X,X,1,2,3],
          	 [X,X,X,X,3,X,2],
          	 [3,X,X,1,2,2,3],
          	 [2,X,3,X,3,2,X],
          	 [2,1,X,1,2,X,3]]
        )


	#puzzle = [[2,2,X],[3,X,3]]

	puzzle.print_all_solutions()

