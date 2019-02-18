

# Function to return the minimum value of three numbers
def min(num1, num2, num3):

    if num1 <= num2 and num1 <= num3:
        return num1
    elif num2 <= num1 and num2 <= num3:
        return num2
    else:
        return num3


# def seqFileToList()
# Takes a string filename as argument, returns a list of dicts
# Each element of the list has the following format:
#
# List[0] = {
#    'seqA': AGTCGGTACGCT...
#    'seqB': TCAGGTTAACAC...
# }

def seqFileToList(filename):
    listOfPairs = list()

    with open(filename, 'r') as file:
        for rawline in file:
            tmp = list()

            for l in rawline.split(','):
                tmp.append(l.strip('\n'))

            listOfPairs.append({'seqA': tmp[0], 'seqB': tmp[1]})

    return listOfPairs


# function to put imp2cost.txt into a 2-d list
def costFileToList(filename):
    rawCostList = list()
    costList = dict()

    with open(filename, 'r') as file:
        for rawline in file:
            line = rawline.strip('\n').split(',')
            rawCostList.append(line)

    for i in range(1, 6):
        for j in rawCostList[i]:
            costList[j] = rawCostList[i][1:]
            break

    return costList


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


# Function to get the cost of aligning letters a and b. Uses costList
# returned by costFileToList().
def cost(costList, a, b):
    if a == b:
        return 0
    else:
        c = letterToIdx(b)
        if c is not None:
            return costList[a][c]
    return None
