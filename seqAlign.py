import functions as fn

# enter the name of the input data file
seqfile = 'imp2input.txt'

# creates a 2-D python list of the entire input file
# ex: seqlist[2][0] is the first sequence of the 3rd pair of sequences.
seqlist = fn.seqFileToList(seqfile)
seqA = seqlist[0][0]
seqB = seqlist[0][1]

#seqA = "AATTCT"
#seqB = "GATAA"

seqA = "ATCC"
seqB = "TCAC"
# enter the name of the cost data file
costfile = 'imp2cost.txt'
# creates a 2-D python list of the cost table
costlist = fn.costFileToList(costfile)

# makeAlignMatrix() returns a 2-D python list
pair = fn.makeAlignMatrix(costlist, seqA, seqB)
E = pair[0]
directions = pair[1]
# print the final matrix, used for algorithm correctness confirmation
fn.printMatrix(E, seqA, seqB)

# the optimal alignment cost is the bottom right element in the matrix
print 'Optimal Alignment Cost: {}'.format(E[len(seqA)][len(seqB)])

path = fn.followPath(directions, len(seqA) -1, len(seqB)-1)
list1, list2 = fn.edit_string(path, seqA, seqB)
filename = "output.txt"
## Testing file
with open(filename, "w") as fp:
	fp.write(list1)
	fp.write("\n")
	fp.write(list2)
	fp.write("\n")
	fp.write(str(E[len(E)-1][len(E[0])-1]))
fp.close()
 
fn.create_out_file(costlist, seqlist)

## Here is the output file created
