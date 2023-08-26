# SISO program allSubsets.py

# Given a set, computes all subsets of that set.

# inString: Represents a set S of strings with elements separated by whitespace.

# returns: All subsets of S, formatted according to the conventions
# described in utils.formatSetOfSets().

# Example:
# >>> allSubsets('4 5 6')
# '{} {4} {5} {4,5} {6} {4,6} {5,6} {4,5,6}'
import utils; from utils import rf
def allSubsets(inString): 
    # the elements from which we can construct subsets
    elems = inString.split()
    # start with an empty list of subsets
    theSubsets = [ ]
    # add the empty set ``[ ]'' to the list of subsets
    theSubsets.append( [ ] )
    # For each element of the input, append copies of all
    # previously computed subsets, but with the additional new element
    # included.
    for element in elems:
        newSets = [ ]
        for thisSet in theSubsets:
            # create a new subset that includes the current element,
            # and append it to the list of subsets
            newSets.append(thisSet + [element])
        # Update the master list of subsets with all the newly created
        # subsets. This doubles the number of subsets in theSubsets.
        theSubsets.extend(newSets)
    return utils.formatSetOfSets(theSubsets) 



def testAllSubsets():
    testvals = [
        ('','{}'),
        ('4','{} {4}'),
        ('4 5 6','{} {4} {5} {4,5} {6} {4,6} {5,6} {4,5,6}'),
    ]
    for (inString, solution) in testvals:
        val = allSubsets(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

