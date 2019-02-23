import sys
import time

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

import random

def genTestFiles():
    sizes = [500,1000,2000,4000,5000]
    letters = ['A','C','T','G']
    for size in sizes:
        filename = "test_" + str(size) + ".txt"
        with open(filename, "w") as fp:
            for i in range(0,10):
                for j in range(0,size):
                    fp.write(random.choice(letters))
                fp.write(',')
                for j in range(0,size):
                    fp.write(random.choice(letters))
                fp.write('\n')


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
    directions = list()
    # add a blank ('-') character to the beggining of each sequence,
    # save the length of each sequence to a variable
    seqA = '-' + Aseq
    seqB = '-' + Bseq
    lenA = len(seqA)
    lenB = len(seqB)



    # calculate the cost for the first column, where seqB[0] = '-'
    for i in range(0, lenA):
        E.append(list())  # each iteration adds a new row to column 0
        directions.append(list())
        if i == 0:  # the very first element, has no previous element
            E[i].append(cost(costlist, seqA[i], '-'))
            directions[i].append(['start'])
        else:
            # the current row gets the cost of the previous row plus the cost
            # of aligning the current letter with '-'
            E[i].append(E[i-1][0] + cost(costlist, seqA[i], '-'))
            directions[i].append(['up'])


    # calculate the cost for the first row, where seqA[0] = '-'
    for j in range(1, lenB):  # start at 1, 0'th element is already calculated
        # Each element of the first row gets the cost of the previous element
        # plus the cost of aligning with '-'
        E[0].append(E[0][j-1] + cost(costlist, '-', seqB[j]))
        directions[0].append(['left'])

    # calculate the cost for the rest of the matrix
    for i in range(1, lenA):
        for j in range(1, lenB):
            dirns = []
            use_j = E[i-1][j] + cost(costlist, seqA[i], '-')
            use_i = E[i][j-1] + cost(costlist, '-', seqB[j])
            use_both = E[i-1][j-1] + cost(costlist, seqA[i], seqB[j])
            E[i].append(min(use_j, use_i, use_both))
            minimum = min(use_j, use_i, use_both)
            if minimum == use_both:
                # direction is diagonal
                dirns.append('diagonal')
            if minimum == use_j:
                dirns.append('up')
            if minimum == use_i:
                dirns.append('left')
            directions[i].append(dirns) 

    return (E, directions)


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

def printWordMatrix(E, seqA, seqB):
    seqA = '-' + seqA
    seqB = '-' + seqB

    sys.stdout.write('    ')
    for i in range(0, len(seqB)):
        sys.stdout.write('{0: <3}'.format(seqB[i]))
    sys.stdout.write('\n')


    for i in range(0, len(E)):
        sys.stdout.write(" {}| ".format(seqA[i]))
        for j in range(0, len(E[i])):
            s = '+'
            printstr = s.join(E[i][j])
            sys.stdout.write("{} ".format(printstr))
            for k in range(0, 17-len(printstr)):
                sys.stdout.write(" ")
        sys.stdout.write("\n")

def runTests():
    seqfiles = ['test_500.txt', 'test_1000.txt', 'test_2000.txt', 'test_4000.txt' , 'test_5000.txt']
    seqLengths = [500, 1000, 2000, 4000, 5000]
    costfile = 'imp2cost.txt'
    costlist = costFileToList(costfile)  # only use costlist via functions
    seqindex = 0
    with open("results.txt", "w+") as results:
        for seqfile in seqfiles:
            seqlist = seqFileToList(seqfile)
            count = 1
            avg = 0
            for line in seqlist:
                seqA = line[0]
                seqB = line[1]
                start = time.time()
                E = makeAlignMatrix(costlist, seqA, seqB)[0]
                end = time.time()
                avg = ((end-start)+(avg)*(count-1))/count
                print(str(avg) + '\n')
                count += 1
            results.write(str(seqLengths[seqindex]) + "\t" + str(avg) + "\n")
            seqindex += 1

def followPath(directions, i, j):
    possiblePaths = []
    minlen = i + j + 1000
    if i == 0 and j == 0:
        return['start'] 

    #sys.stdout.write("{} {} {} \n".format(i,j, directions[i][j]))


    # try each path that is listed in the directions list for E[i][j]
    for dirn in directions[i][j]:
        # left path goes to E[i-1][j]
        if dirn == 'left':
            path = followPath(directions, i, j-1)
            path.append(dirn)
            possiblePaths.append(path)
        if dirn == 'up':
            path = followPath(directions, i-1, j)
            path.append(dirn)
            possiblePaths.append(path)
        if dirn == 'diagonal':
            path = followPath(directions, i-1, j-1)
            path.append(dirn)
            possiblePaths.append(path)

    for path in possiblePaths:
        if len(path) < minlen:
            minlen = len(path)

    for option in possiblePaths:
        if len(option) == minlen:
            return option


    return ['fail']


def wordFromBacktrace(path, seq, left_is_space):
    newWord = ""
    i = 0
    if(left_is_space):
        for dirn in path:
            if dirn == 'left':
                newWord += '-'
            elif dirn == 'up':
                newWord += seq[i]
                i += 1
            elif dirn == 'diagonal':
                newWord += seq[i]
                i += 1
            if dirn == 'fail':
                return ""
    else:
        for dirn in path:
            if dirn == 'left':
                newWord += seq[i]
                i += 1
            elif dirn == 'up':
                newWord += '-'
            elif dirn == 'diagonal':
                newWord += seq[i]
                i += 1
            if dirn == 'fail':
                return ""

    return newWord

def getAlignmentCost(costList, seqA,seqB):
    total = 0
    for i in range(len(seqA)):
        total += cost(costList, seqA[i],seqB[i])

    return total

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
# ************* Example usage **********************************
def main():
    seqfile = 'imp2input.txt'    
    costfile = 'imp2cost.txt'
    costlist = costFileToList(costfile)  # only use costlist via functions
    seqlist = seqFileToList(seqfile)

    with open('imp2output.txt', 'w') as outputfile:
        for line in seqlist:
            seqA = line[0]
            seqB = line[1]

            res = makeAlignMatrix(costlist, seqA, seqB)
            E = res[0]
            directions = res[1]
            # for line in directions:
            #     print(line)
            answer = followPath(directions, len(seqA), len(seqB))
            alignment1 = wordFromBacktrace(answer, seqB, False)
            alignment2 = wordFromBacktrace(answer, seqA, True)
            outstring = alignment1 + ',' + alignment2 + ':' + str(getAlignmentCost(costlist,alignment1,alignment2)) + '\n'
            outputfile.write(outstring)
    #printWordMatrix(directions, seqA, seqB)
    #printWordMatrix(directions, seqA, seqB)
    # generate the optimum allignment from E and the direction matrix and output to file

    # print "SeqA: {}\nSeqB: {}\n".format(seqA, seqB)
    # cost1 = cost(costlist, 'A', 'G')
    # cost2 = cost(costlist, '-', 'T')
    # cost3 = cost(costlist, 'C', 'T')


if __name__ == "__main__":
    main()
