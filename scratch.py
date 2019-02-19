import helpers
import sys


seqfile = 'imp2input.txt'
seqlist = helpers.seqFileToList(seqfile)

costfile = 'imp2cost.txt'
costlist = helpers.costFileToList(costfile)

seqA = '-' + seqlist[0][0]
seqB = '-' + seqlist[0][1]
lenA = len(seqlist[0][0])
lenB = len(seqlist[0][1])

E = list()
for i in range(0, lenA):
    E.append(list())
    # print "seqA[{}]: {}".format(i, seqA[i])
    E[i].append(helpers.cost(costlist, seqA[i], seqB[0]))

for j in range(1, lenB):
    E[0].append(helpers.cost(costlist, seqA[0], seqB[j]))


for i in range(1, lenA):
    for j in range(1, lenB):
        E[i].append(min(E[i-1][j] +1, E[i][j-1] +1, E[i-1][j-1] + helpers.cost(costlist, seqA[i], seqB[j])))


for i in E:
    for j in i:
        if j/10 < 1:
            sys.stdout.write("{} ".format(j))
        else:
            sys.stdout.write("{}".format(j))
    print "\n"
