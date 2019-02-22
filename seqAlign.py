import functions as fn

# enter the name of the input data file
seqfile = 'imp2input.txt'

# creates a 2-D python list of the entire input file
# ex: seqlist[2][0] is the first sequence of the 3rd pair of sequences.
seqlist = fn.seqFileToList(seqfile)
#seqA = seqlist[0][0]
#seqB = seqlist[0][1]

#seqA = "ATCC"
#seqB = "TCAC"

seqA = "TACG"
seqB = "TGG"
# enter the name of the cost data file
costfile = 'imp2cost.txt'
# creates a 2-D python list of the cost table
costlist = fn.costFileToList(costfile)

# makeAlignMatrix() returns a 2-D python list
E = fn.makeAlignMatrix(costlist, seqA, seqB)

# print the final matrix, used for algorithm correctness confirmation
fn.printMatrix(E, seqA, seqB)

# the optimal alignment cost is the bottom right element in the matrix
print 'Optimal Alignment Cost: {}'.format(E[len(seqA)][len(seqB)])

list1, list2, min = fn.backTrace(E, seqA, seqB)
str1 = "".join(list1)
str2 = "".join(list2)
filename = "output.txt"
with open(filename, "w") as fp:
	fp.write(str1)
	fp.write("\n")
	fp.write(str2)
	fp.write("\n")
	fp.write(str(min))
