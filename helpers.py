

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


# ************* Example usage **********************************

