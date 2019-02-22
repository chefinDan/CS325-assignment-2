import sys

# *********************************************************
# Example usage of the functions can be found at the bottom
# of the page
# *********************************************************


#####################################################
# function seqFileToList()
# Takes a string filename as argument, opens the file and
# returns a list of dicts. Each element of the list has the
# following format:
#
# List[0] = [
#    [AGTCGGTACGCT...]
#    [TCAGGTTAACAC...]
# }


def seqFileToList(filename):
    # list structure to store gene sequence data of the entire file
    listOfPairs = list()

    with open(filename, 'r') as file:
        for rawline in file:  # get the next unformatted line and put into rawline
            tmp = list()  # list structure for the actual sequence data

            # Split rawline at the comma and loop through the resulting two strings
            # strip each string of newline chars and add to the tmp list
            for l in rawline.split(','):
                tmp.append(l.strip('\n'))

            # append a list object to main gene sequence list
            listOfPairs.append([tmp[0], tmp[1]])

    return listOfPairs


# ######################################################
# function to put imp2cost.txt into a 2-d list.
# Takes a string filename as argument, opens the corresponding file,
# formats the costfile information and returns a 2-d list.
# The costList returned is not be accessed directly, but passed to other
# functions where needed.
def costFileToList(filename):
    rawCostList = list()  # tmp list object
    costList = list()  # list object to be returned

    # open file named <filename>, loop through the lines, appending
    # the formatted line to rawCostList
    with open(filename, 'r') as file:
        for rawline in file:
            line = rawline.strip('\n').split(',')
            rawCostList.append(line)

    # Start at 1, to avoid copying the title row of the cost file.
    # Append each row from costFile to costList, again starting at 1 to
    # avoid copying the title column.
    for i in range(1, 6):
        costList.append(rawCostList[i][1:])
        # print costList

    return costList


# ######################################################################
# Function to get the cost of aligning letters a and b. Uses costList
# returned by costFileToList().
#
def cost(costList, a, b):
    if a == b:
        return 0
    else:
        c = letterToIdx(a)
        d = letterToIdx(b)
        if c is not None and d is not None:
            return int(costList[c][d])
    return None


# helper to convert a Gene letter to it's corresponding array index
def letterToIdx(x):
    letters = {
        '-': 0,
        'A': 1,
        'T': 2,
        'G': 3,
        'C': 4
    }

    return letters.get(x)


def makeAlignMatrix(costlist, Aseq, Bseq):
    # declare the alignment matrix E to be a python list
    E = list()

    # add a blank ('-') character to the beggining of each sequence,
    # save the length of each sequence to a variable
    seqA = '-' + Aseq
    seqB = '-' + Bseq
    lenA = len(seqA)
    lenB = len(seqB)

    # calculate the cost for the first column, where seqB[0] = '-'
    for i in range(0, lenA):
        E.append(list())  # each iteration adds a new row to column 0
        if i == 0:  # the very first element, has no previous element
            E[i].append(cost(costlist, seqA[i], '-'))
        else:
            # the current row gets the cost of the previous row plus the cost
            # of aligning the current letter with '-'
            E[i].append(E[i-1][0] + cost(costlist, seqA[i], '-'))

    # calculate the cost for the first row, where seqA[0] = '-'
    for j in range(1, lenB):  # start at 1, 0'th element is already calculated
        # Each element of the first row gets the cost of the previous element
        # plus the cost of aligning with '-'
        E[0].append(E[0][j-1] + cost(costlist, '-', seqB[j]))

    # calculate the cost for the rest of the matrix
    for i in range(1, lenA):
        for j in range(1, lenB):
            use_j = E[i-1][j] + cost(costlist, seqA[i], '-')
            use_i = E[i][j-1] + cost(costlist, '-', seqB[j])
            use_both = E[i-1][j-1] + cost(costlist, seqA[i], seqB[j])
            E[i].append(min(use_j, use_i, use_both))

    return E


def printMatrix(E, seqA, seqB):
    seqA = '-' + seqA
    seqB = '-' + seqB

    sys.stdout.write('    ')

    for i in range(0, len(seqB)):
        sys.stdout.write('{0: <3}'.format(seqB[i]))
    sys.stdout.write('\n')
    sys.stdout.write('   ')

    for i in range(0, len(seqB)):
        sys.stdout.write("{}".format('---'))
    sys.stdout.write('\n')

    for i in range(0, len(seqA)):
        sys.stdout.write(" {}| ".format(seqA[i]))
        for j in range(0, len(seqB)):
            if E[i][j]/10 < 1:
                sys.stdout.write("{}  ".format(E[i][j]))
            else:
                sys.stdout.write("{} ".format(E[i][j]))
        sys.stdout.write("\n")

def backTrace(E, SeqA, SeqB):
	lenght1 = len(SeqA)
	lenght2 = len(SeqB)
	xLength = len(E[0]) - 1				#rows
	yLength = len(E) - 1				#columns
	print xLength
	print yLength
	trace = 0
	traceList = []
	minCost = E[yLength][xLength]
	while(not(xLength == 0 and yLength == 0)):
		cost = E[yLength][xLength]
		aboveCost = E[yLength -1][xLength]
		leftCost = E[yLength][xLength-1]
		diagCost = E[yLength-1][xLength-1]
		print cost
		if (yLength != 0 and diagCost < cost and diagCost <= leftCost and diagCost <= aboveCost):
			xLength, yLength = xLength-1, yLength - 1
			print "diagnonal"
			trace = trace + 1
			traceList.append('d')			
		elif (xLength != 0 and leftCost < cost and leftCost < aboveCost):
			xLength, yLength = xLength-1, yLength
			print "left"
			trace = trace + 1
			traceList.append('l')
		elif (yLength != 0 and aboveCost < cost):
			xLength, yLength = xLength, yLength-1
			print "above"
			trace = trace + 1
			traceList.append('u')
		elif  (xLength != 0 and yLength != 0 and diagCost == cost):
			xLength, yLength = xLength-1, yLength-1
			print "diagnonal"
			trace = trace + 1
			traceList.append('=')
				
			
	print traceList
	print SeqA, SeqB
	list1, list2 = edit_string(traceList, trace, SeqA, SeqB)
	print list1
	print list2
	return list1, list2, minCost
	
def edit_string(path, pathLength, seqA, seqB):
	lenB = len(seqB)
	editB = []					# new edited string
	lenA = len(seqA)
	editA = []					# new edited string
	# edit string A
	while lenA > 0:
		for i in range(0, pathLength):
			if path[i] == 'd': 				# if it is diagnonal and not equal to the previous cost add a space
				#print "align", editA
				lenA = lenA -1
				editA.append(seqA[lenA])
				editA.append('-')
				
				#print "after align", editA
			elif path[i] == '=':			# if the cost is the same do nothing
				#print "align", editA
				lenA = lenA -1
				#print lenA, seqA[lenA]
				editA.append(seqA[lenA])
				#print "after align", editA
			elif path[i] == 'l':			# if the trace went left add a space to first string
				#print "insert", editA
				editA.append('-')
				#print "after", editA
			elif path[i] == 'u':			# if trace went up, do nothing
				#print "deletion", editA
				lenA = lenA -1
				editA.append(seqA[lenA])
				#print "deletion", editA
	# edit string B
	while lenB > 0:
		for i in range(0, pathLength):
			if path[i] == 'd':				# if it is diagnonal and not equal to the previous cost add a space 
				#print "align"
				lenB = lenB -1
				editB.append('-')
				editB.append(seqB[lenB])
			elif path[i] == '=':			# if the cost is the same do nothing
				#print "align"
				lenB = lenB -1
				editB.append(seqB[lenB])
			elif path[i] == 'l':			# if the trace went left do nothing
				#print "insert"
				lenB = lenB -1
				editB.append(seqB[lenB])
			elif path[i] == 'u':			# if the trace went up add a space
				#print "deletion"
				editB.append('-')
	return editA[::-1], editB[::-1]			# strings are in reverse so I reversed to normal here
	

# ************* Example usage **********************************
# seqfile = 'imp2input.txt'
# seqlist = seqFileToList(seqfile)
# seqA = seqlist[0][0]
# seqB = seqlist[0][1]
# print "SeqA: {}\nSeqB: {}\n".format(seqA, seqB)
#
# costfile = 'imp2cost.txt'
# costlist = costFileToList(costfile)  # only use costlist via functions
# cost1 = cost(costlist, 'A', 'G')
# cost2 = cost(costlist, '-', 'T')
# cost3 = cost(costlist, 'C', 'T')
#
# min = min(cost1, cost2, cost3)
#
# print min