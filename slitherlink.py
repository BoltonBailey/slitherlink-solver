
X = None

ROWS = 7
COLS = 7

# A pretty printer for displaying a slitherlink board, along with a partial solution
def prettyprint(puzzle, solution):
	symbols_array = [["  "] * (2*COLS+1) for i in range (2*ROWS+1)]

	for i in range(2*ROWS+1):
		for j in range(2*COLS+1):
			if i % 2 == 0:
				if j % 2 == 0:
					symbols_array[i][j] = "+ "
				else:
					if not ((i/2, j/2), (i/2, j/2 + 1)) in solution:
						symbols_array[i][j] = ". "
					elif solution[((i/2, j/2), (i/2, j/2 + 1))]:
						symbols_array[i][j] = "- "
					else:
						symbols_array[i][j] = "  "
			else:
				if j % 2 == 0:
					if not ((i/2, j/2), (i/2+ 1, j/2 )) in solution:
						symbols_array[i][j] = ". "
					elif solution[((i/2, j/2), (i/2+ 1, j/2 ))]:
						symbols_array[i][j] = "| "
					else:
						symbols_array[i][j] = "  "
				else:
					if not puzzle[i/2][j/2] == None:
						symbols_array[i][j] = str(puzzle[i/2][j/2]) + " "

			symbols_array[i][j]
		
	
	for i in range(2*ROWS+1):
		newline = ""
		for j in range(2*COLS+1):
			newline += symbols_array[i][j]
		print newline



def solve(puzzle):
	current_solution = {}
	return possible_partial_solve(puzzle, current_solution)


list_of_lines = []
for i in range(ROWS+1):
	for j in range(COLS):
		list_of_lines.append(((i,j),(i,j+1)))
for i in range(ROWS):
	for j in range(COLS+1):
		list_of_lines.append(((i,j),(i+1,j)))


list_of_lines = sorted(list_of_lines)
set_of_lines = set(list_of_lines)

# returns solution if possible, none if not.
def possible_partial_solve(puzzle, partial_solution):
	print prettyprint(puzzle, partial_solution)

	if test_for_violation(puzzle, partial_solution):
		return None
	else:
		next_line = None
		for line in list_of_lines:
			if line not in partial_solution:
				next_line = line
				break
		if next_line == None:
			# no violations and no more lines. This is correct.
			return partial_solution
		else:
			partial_solution[next_line] = True
			solution = possible_partial_solve(puzzle, partial_solution)
			if solution != None:
				return solution
			partial_solution[next_line] = False
			solution = possible_partial_solve(puzzle, partial_solution)
			if solution != None:
				return solution
			del partial_solution[next_line]
			return None


# Given a puzzle and a partial solution, checks that the partial solution does 
# not directly break any rules.
def test_for_violation(puzzle, partial_solution):
	# Test intersections for no dead ends or forks
	vertices = [(i, j) for i in range(ROWS+1) for j in range(COLS+1)]
	for vertex in vertices:
		if test_for_vertex_violation(puzzle, partial_solution, vertex):
			return True
	#Test squares for right number of lines
	squares = [(i, j) for i in range(ROWS) for j in range(COLS)]
	for square in squares:
		if test_for_square_violation(puzzle, partial_solution, square):
			return True
	# Test for no two cycles
	return False


# Helper function that determines, for a vertex, if the rule against no 
# branchings or dead ends has been violated for that vertex.
def test_for_vertex_violation(puzzle, partial_solution, vertex):
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
def test_for_square_violation(puzzle, partial_solution, square):
	i, j = square
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


	solution = solve(puzzle)

	prettyprint(puzzle, solution)

