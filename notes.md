#Functions

 #^*************************************************************************^#
 # Function to take set of DNA data from file, (newline delimited), and
 # produce two arrays, both of length = max{len(pair_a), len(pair_b)}

 ### def convertFileLineToArray(file):
 ###    return: pairA[], pairB[]



 #^**************************************************************************^#
 # Function to read imp2cost.txt into a data structure and return it.

 ### def costGraphToArray(File imp2Cost.txt):
 ###    return: costArray



 #^**************************************************************************^#
 # Function to calculate the diff cost for two letters. Reads cost data from
 # costArray.

 ### def cost(costArray, letter_x, letter_y):
 ###    return: int(cost)



 #^**************************************************************************^#
 # Function to return the min value of three possible edit costs. E is the
 # table of all costs, ie edit distance table.

 ### def min(E(i-1,j) + cost(i,j), E(i,j-1) + cost(i,j), E(i-1,j-1) + cost(i, j))
 ###    return int(min)
