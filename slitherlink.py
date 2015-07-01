
# For convenience

X = None

# Count of rows and columns

ROWS = 7
COLS = 7

# lists and sets associated with objects in the board

list_of_lines = []
for i in range(ROWS+1):
	for j in range(COLS):
		list_of_lines.append(((i,j),(i,j+1)))
for i in range(ROWS):
	for j in range(COLS+1):
		list_of_lines.append(((i,j),(i+1,j)))


list_of_lines = sorted(list_of_lines)
set_of_lines = set(list_of_lines)

vertices = [(i, j) for i in range(ROWS+1) for j in range(COLS+1)]
set_of_vertices = set(vertices)

squares = [(i, j) for i in range(ROWS) for j in range(COLS)]
set_of_squares = set(squares)


# A pretty printer for displaying a slitherlink board, along with a partial solution
def prettyprint(puzzle, solution):
	symbols_array = [[""] * (2*COLS+1) for i in range (2*ROWS+1)]

	for i in range(2*ROWS+1):
		for j in range(2*COLS+1):
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
					if not puzzle[i/2][j/2] == None:
						symbols_array[i][j] = " " + str(puzzle[i/2][j/2]) + " "
					else:
						symbols_array[i][j] = "   "


			symbols_array[i][j]
		
	
	for i in range(2*ROWS+1):
		newline = ""
		for j in range(2*COLS+1):
			newline += symbols_array[i][j]
		print newline

	print
	print
	print


# Prints out all possible solutions
def print_all_solutions(puzzle):
	list_of_solutions = list_solve(puzzle)
	if len(list_of_solutions) == 0:
		print "No solutions found"
	else:
		for solution in list_of_solutions:
			prettyprint(puzzle, solution)



# returns a list of solutions to the given puzzle that extend the given partial solution
# Implemented iteratively
def list_solve(puzzle):

	# Partial solutions initially are just the empty solution
	partial_solutions = [{}]
	solutions = []

	while partial_solutions:

		# Retrieve a partial
		partial_solution = partial_solutions.pop()

		next_line = None
		for line in list_of_lines:
			if line not in partial_solution:
				next_line = line
				break

		# Test to see if the given partial solution is full.
		if next_line == None:
			# Since each line added was tested for violations, this is good. Place in solutions and continue
			solutions.append(partial_solution)
			continue

		# At this point, we know that the solution is not full, and line is currently empty

		# We copy partial solution into two new partial solutions, and put them in the list
		partial_solution_fill = dict(partial_solution)
		partial_solution_fill[next_line] = True
		if not line_violation(puzzle, partial_solution_fill, next_line):
			partial_solutions.append(partial_solution_fill)

		partial_solution_empty = dict(partial_solution)
		partial_solution_empty[next_line] = False
		if not line_violation(puzzle, partial_solution_empty, next_line):
			partial_solutions.append(partial_solution_empty)

	return solutions

	


# Given a puzzle and a partial solution, checks that the partial solution does 
# not directly break any rules.
def violation(puzzle, partial_solution):
	# Test intersections for no dead ends or forks
	
	for vertex in vertices:
		if vertex_violation(puzzle, partial_solution, vertex):

			return True
	#Test squares for right number of lines
	
	for square in squares:
		if square_violation(puzzle, partial_solution, square):

			return True
	# Test for no two cycles
	# TODO

	# If no violations are found return False
	return False


# function that tests a line to see if there is a violation associated with that line
def line_violation(puzzle, partial_solution, line):
	assert line in partial_solution

	vertex0 = line[0]
	i0, j0 = vertex0

	vertex1 = line[1]
	i1, j1 = vertex1

	# test the vertices
	if vertex_violation(puzzle, partial_solution, vertex0):
		return True
	if vertex_violation(puzzle, partial_solution, vertex1):
		return True

	# test the squares
	square0 = vertex0
	if square0 in set_of_squares:
		if square_violation(puzzle, partial_solution, square0):
			return True

	if j1 > j0:
		square1 = (i0-1, j0)
	else:
		square1 = (i0, j0-1)

	if square1 in set_of_squares:
		if square_violation(puzzle, partial_solution, square1):
			return True

	# Todo: test against multiple cycles

	return False


# Helper function that determines, for a vertex, if the rule against no 
# branchings or dead ends has been violated for that vertex.
def vertex_violation(puzzle, partial_solution, vertex):
	i, j = vertex
	on = 0
	off = 0
	empty = 0
	for line in [((i,j),(i,j+1)),
	             ((i,j),(i+1,j)),
	             ((i,j-1),(i,j)),
	             ((i-1,j),(i,j))]:
		if line not in set_of_lines:
			pass
		elif not line in partial_solution:
			empty += 1
		elif partial_solution[line]:
			on += 1
		else:
			off += 1
	if on > 2 or (empty == 0 and on == 1):
		return True
	return False

# Helper function that determines, for a square, if the rule for number of 
# lines around that square has been broken
def square_violation(puzzle, partial_solution, square):
	i, j = square

	assert square in set_of_squares

	if puzzle[i][j] == None:
		return False

	on = 0
	off = 0
	empty = 0

	for line in [((i,j),(i,j+1)),
		         ((i,j),(i+1,j)),
			     ((i,j+1),(i+1,j+1)),
			     ((i+1,j),(i+1,j+1))]:
		if not line in partial_solution:
			empty += 1
		elif partial_solution[line]:
			on += 1
		else:
			off += 1

	if (puzzle[i][j] > on + empty) or (puzzle[i][j] < on):
		return True
	return False




if __name__ == "__main__":



	puzzle = [[3,2,2,2,X,X,X],
          	  [2,2,X,3,X,3,2],
          	  [X,X,X,X,1,2,3],
          	  [X,X,X,X,3,X,2],
          	  [3,X,X,1,2,2,3],
          	  [2,X,3,X,3,2,X],
          	  [2,1,X,1,2,X,3]]


	#puzzle = [[2,2,X],[3,X,3]]

	print_all_solutions(puzzle)

