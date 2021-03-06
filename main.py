

#------
import slitherlink
import time
import urllib2

def retrieve_from_source(string):

	for line in string.split("\n"):
		if line.startswith("<table onContextMenu=\"return false\" id=\"LoopTable\""):
			table_line = line

	list_of_inputs = []
	for i in range(len(table_line)):

		if table_line[i:].startswith("<td align=\"center\" ><"):
			list_of_inputs.append(None)
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

	return slitherlink.SlitherlinkPuzzle(array)	

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
			list_of_inputs.append(None)
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

	return slitherlink.SlitherlinkPuzzle(array)


def retrieve_from_site():
	response = urllib2.urlopen("http://www.puzzle-loop.com/?size=9")
	page_source = response.read()
	return retrieve_from_source(page_source)


i = 0
time_total = 0
while __name__ == "__main__":

	print "Number of puzzles", i
	


	retrieval_start = time.clock()

 	print "Beginning retrieval of puzzle..." 
	puzzle = retrieve_from_site()
	print "Puzzle created in", time.clock() - retrieval_start, "seconds" 

	solution_start = time.clock()

	puzzle.print_all_solutions()

	print "Puzzle solved in", time.clock() - solution_start, "seconds"

	i += 1
	time_total += time.clock() - solution_start
	print "Average time", time_total/i



