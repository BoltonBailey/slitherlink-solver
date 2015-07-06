
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

		self.lines = []

		# First the horizontal lines
		for i in range(self.rows+1):
			for j in range(self.cols):
				self.lines.append(((i,j),(i,j+1)))
		# Then the vertical
		for i in range(self.rows):
			for j in range(self.cols+1):
				self.lines.append(((i,j),(i+1,j)))

		self.lines = sorted(self.lines)

		# We now put these in set form, for quick membership tests

		self.set_of_lines = set(self.lines)


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

			self.prettyprint(partial_solution)

			# Test to see if the given partial solution is full.
			if len(partial_solution) == len(self.lines):
				# The given partial solution is full.
				# Since each line added was tested for violations, this is 
				# valid. Place in solutions and continue
				solutions.append(partial_solution)
				continue

			# Find, now, an empty line
			next_line = None
			for line in self.lines:
				if line not in partial_solution:
					next_line = line
					
					# We check to see if either of the two new dicts we 
					# create will be eliminated immediately. If so, this is 
					# favorable, so we break, and choose this line.
					partial_solution[next_line] = True
					if self.line_violation(partial_solution, next_line):
						break

					partial_solution[next_line] = False
					if self.line_violation(partial_solution, next_line):
						break

					del partial_solution[next_line]



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

	

	def violation(self, complete_solution):
		""" This method, given a complete solution, checks if the complete 
		solution directly breaks any rules. """

		assert len(complete_solution) == len(self.lines)

		# Test intersections for no dead ends or forks
		for vertex in self.vertices:
			if self.vertex_violation(complete_solution, vertex):
				return True

		# Test squares for right number of lines
		for square in self.squares:
			if self.square_violation(complete_solution, square):
				return True

		# Test for no two cycles

		# Find a filled line

		for line in self.lines:
			if complete_solution[line]:
				break
		
		if self.loop_violation(complete_solution, line):
			return True

		# If no violations are found return False
		return False


	def line_violation(self, partial_solution, line):
		""" This method, given a partial solution and a line, checks if the 
		determination of that line breaks any vertex or square rules for the 
		adjacent squares and connected vertices. """

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

		if self.loop_violation(partial_solution, line):
			return True

		return False


	def vertex_violation(self, partial_solution, vertex):
		""" This method, given a partial solution and a vertex, checks if the 
		rule against no branchings or dead ends has been violated for that 
		vertex. """

		# Count the edges from this vertex which are filled, empty and 
		# undetermined
		filled = 0
		empty = 0
		undetermined = 0

		for line in get_adjacent_lines(vertex):
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

	def loop_violation(self, partial_solution, line):
		""" This method, given a partial_solution and a line, determines if that 
		line is in a loop that is not a solution to the board"""

		if line not in partial_solution or partial_solution[line] == False:
			return False

		# A running solution of all lines found in the loop
		loop_solution = {}

		# Iterate around the loop
		current_line = line
		loop_solution[line] = True
		current_vertex = line[1]

		while current_vertex != line[0]:
			# We first find the next line in the sequence:
			next_line = None
			for new_line in get_adjacent_lines(current_vertex):
				if new_line in partial_solution and partial_solution[new_line]:
					if new_line != current_line:
						# This new_line is correct
						next_line = new_line
						break
			
			# If no next_line was found, we have a dead end, so no loop violation
			if next_line == None:
				return False
			
			# Now, we change to this new edge, and add it to the loop
			current_line = next_line
			loop_solution[current_line] = True

			# We now switch the vertex to the other vertex of the line
			if current_vertex == current_line[1]:
				current_vertex = current_line[0]
			else:
				current_vertex = current_line[1]

		# We now at this point that there is a loop, and it is represented in the loop solution
		# We must determine if there are any filled lines in the partial solution outside the loop
		# And if the loop constitues a valid complete solution.

		for l in partial_solution:
			if partial_solution[l] and l not in loop_solution:
				# We have located a filled line outside the loop. This is a violation.
				return True

		# We now know that the loop contains all filled lines. We must check that the loop solution has no vertex or square violations
		for l in self.set_of_lines:
			if l not in loop_solution:
				loop_solution[l] = False

		assert len(loop_solution) == len(self.lines)

		# Test vertices for no dead ends or forks
		for vertex in self.vertices:
			if self.vertex_violation(loop_solution, vertex):
				return True

		# Test squares for right number of lines
		for square in self.squares:
			if self.square_violation(loop_solution, square):
				return True

		# We have found no violations. This is a valid solution.
		return False

		




def get_adjacent_lines(vertex):
	""" Returns a list of lines attached to the given vertex """

	# Unpack the vertex
	i, j = vertex

	return [((i,j),(i,j+1)),
		    ((i,j),(i+1,j)),
		    ((i,j-1),(i,j)),
		    ((i-1,j),(i,j))]




def retrive_from_file(filename):
	""" Given a filename, parses the file to return a slitherlink instance. 
	This parser is designed to retrieve from the source code of 
	puzzle-loop.com """
	
	file = open(filename, "r")

	table_line = None

	for line in file:
		if line.startswith("<table onContextMenu=\"return false\" id=\"LoopTable\""):
			table_line = line

	list_of_inputs = []
	for i in range(len(table_line)):

		if table_line[i:].startswith("<td align=\"center\" ><"):
			list_of_inputs.append(X)
		if table_line[i:].startswith("<td align=\"center\" >0<"):
			list_of_inputs.append(0)
		if table_line[i:].startswith("<td align=\"center\" >1<"):
			list_of_inputs.append(1)
		if table_line[i:].startswith("<td align=\"center\" >2<"):
			list_of_inputs.append(2)
		if table_line[i:].startswith("<td align=\"center\" >3<"):
			list_of_inputs.append(3)

	size = len(list_of_inputs)
	if size == 25:
		rows = 5
		cols = 5
	if size == 49:
		rows = 7
		cols = 7
	if size == 100:
		rows = 10
		cols = 10
	if size == 225:
		rows = 15
		cols = 15
	if size == 400:
		rows = 20
		cols = 20
	if size == 750:
		rows = 30
		cols = 25
	if size == 1200:
		rows = 40
		cols = 30

	array = [[list_of_inputs[i * cols + j] for j in range(cols)] for i in range(rows)]

	return SlitherlinkPuzzle(array)




if __name__ == "__main__":

 	print "Beginning retrieval of puzzle..." 
	puzzle = retrive_from_file("puzzle.html")
	print "Puzzle created"

	puzzle.print_all_solutions()



