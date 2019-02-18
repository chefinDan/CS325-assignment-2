# def fileToList()
# Takes a string filename as argument, returns a list of dicts
# Each element of the list has the following format:
#
# List[0] = {
#    'seqA': AGTCGGTACGCT...
#    'seqB': TCAGGTTAACAC...
# }


def fileToList(filename):
    E = list()

    with open(filename, 'r') as file:
        for rawline in file:
            tmp = list()

            for l in rawline.split(','):
                tmp.append(l.strip('\n'))

            E.append({'seqA': tmp[0], 'seqB': tmp[1]})

    return E


# def getSeq(E[n], int seq)
# This function takes a dict object from E and a number indicating
# which sequence is wanted, the first or second.
def getSeq(dic, num):
    if num == 1:
        return dic['seqA']
    elif num == 2:
        return dic['seqB']
    else:
        return None
