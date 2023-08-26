# SISO program all3Sets.py

# Given a set, computes all subsets of size 3.

# inString: Represents a set S of strings with elements separated by whitespace.

# returns: All subsets of S containing exactly 3 elements, formatted
# according to the conventions described in utils.formatSetOfSets().

# Example:
# >>> all3Sets('4 5 6 7')
# '{4,5,6} {4,5,7} {4,6,7} {5,6,7}'
import utils; from utils import rf
def all3Sets(inString): 
    # the elements from which we can construct subsets
    elems = inString.split()
    # start with an empty list of 3-sets
    threeSets = [ ]
    # append each 3-set to the list threeSets
    for i in range(0,len(elems)): 
        for j in range(i+1,len(elems)):
            for k in range(j+1,len(elems)):
                this3Set = [ elems[i], elems[j], elems[k] ]
                threeSets.append(this3Set)
    return utils.formatSetOfSets(threeSets) 

def testAll3Sets():
    testvals = [
        ('',''),
        ('4 5',''),
        ('4 5 6','{4,5,6}'),
        ('4 5 6 7','{4,5,6} {4,5,7} {4,6,7} {5,6,7}'),
        ('4 5 6 7 8','{4,5,6} {4,5,7} {4,5,8} {4,6,7} {4,6,8} {4,7,8} {5,6,7} {5,6,8} {5,7,8} {6,7,8}'),
    ]
    for (inString, solution) in testvals:
        val = all3Sets(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

