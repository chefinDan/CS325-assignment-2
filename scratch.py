import helpers
import sys


seqfile = 'imp2input.txt'
seqlist = helpers.seqFileToList(seqfile)

costfile = 'imp2cost.txt'
costlist = helpers.costFileToList(costfile)

seqA = '-' + seqlist[2][0]
seqB = '-' + seqlist[2][1]
lenA = len(seqA)
lenB = len(seqB)

E = list()

# calculate the cost for the first column, where seqB[0] = '-'
for i in range(0, lenA):
    E.append(list())
    if i == 0:
        E[i].append(helpers.cost(costlist, seqA[i], '-'))
    else:
        E[i].append(E[i-1][0] + helpers.cost(costlist, seqA[i], '-'))

# calculate the cost for the first row, where seqA[0] = '-'
for j in range(1, lenB):
        E[0].append(E[0][j-1] + helpers.cost(costlist, '-', seqB[j]))


# calculate the cost for the rest of the matrix
for i in range(1, lenA):
    for j in range(1, lenB):
        E[i].append( min(E[i-1][j] + helpers.cost(costlist, seqA[i], '-'),
                         E[i][j-1] + helpers.cost(costlist, '-', seqB[j]),
                         E[i-1][j-1] + helpers.cost(costlist, seqA[i], seqB[j])))

# print the final matrix, used for algo correctness confirmation
helpers.printMatrix(E, seqA, seqB)
