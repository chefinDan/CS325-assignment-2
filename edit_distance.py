import sys
from helpers import seqFileToList
from helpers import costFileToList
from helpers import cost

def edit_distance(seq1, seq2, list):
	leng1 = len(seq1)
	leng2 = len(seq2)
	x =[[0]*(leng2+1) for _ in range(leng1+1)]		#initialization of table
	for i in range(0,leng1+1): 		#initialization of base case values

		x[i][0]=i
	for j in range(0,leng2+1):

		x[0][j]=j
	#creating the table to get min number of edits needed to make
	for i in range (1,leng1+1):

		for j in range(1,leng2+1):

			if seq1[i-1]==seq2[j-1]:
				x[i][j] = x[i-1][j-1] 

			else :
			#code breaks in this line, it works as a basic edit distance table, still trying to incorporate
			#x[i][j]= min(cost(list, x[i], x[j-1]), cost(list, x[i-1], x[j]), cost(list, x[i-1], x[j-1]) )+1
			# doing this:
			#x[i][j]= min(cost(list, seq[i], seq2[j-1]), cost(list, seq1[i-1], seq2[j]), cost(list, seq1[i-1], seq2[j-1]) )+1
			#breaks and goes out of range, have to figure out how to put this together 
				x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1 #creates a default edit table without costs list

	return x[i][j]

def main():
	seqfile = "imp2input.txt"
	seqlist = seqFileToList(seqfile)
	seqA = seqlist[0][0]
	seqB = seqlist[0][1]
	print "SeqA: {}\nSeqB: {}\n".format(seqA, seqB)
	costfile = "imp2cost.txt"
	costlist = costFileToList(costfile)  # only use costlist via functions
	cost1 = cost(costlist, 'A', 'G')
	cost2 = cost(costlist, '-', 'T')
	cost3 = cost(costlist, 'C', 'T')

	min_num = min(cost1, cost2, cost3)
	length = len(seqlist)
	print min_num
	minlist = []
	for i in range(length):
		minlist.append(edit_distance(seqlist[i][0], seqlist[i][1], costlist)) #just grabs the list of min edits for each pair
	print minlist
	return

if(__name__ == "__main__"):
    main()