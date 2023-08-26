# SISO program partition.py

# Solves the computational problem Partition. Given an input which is
# a string representing a list of integer weights, it searches for a
# feasible partition i.e. a subset of the weights that sums to exactly
# half the total weight.
# The recursive search algorithm enumerates all subsets of the weights
# and therefore requires exponential time in the worst case.

# inString: the integer weights are separated by whitespace from each
# other.

# returns: If a feasible partition exists, it is returned formatted as a
# sequence of weights separated by space characters. Otherwise 'no' is
# returned.

# Example:
# >>> partition('6 6 7 7')
# '6 7'
import utils; from utils import rf
from packing import packing
def partition(inString):
    weights = [int(x) for x in inString.split()]
    totalWeight = sum(weights)
    if totalWeight%2 != 0:
        # If the sum of the weights isn't even, no partition is
        # possible.
        return 'no'
    else:
        # Reduce the problem to an instance of Packing.
        targetWeight = str(int(totalWeight/2))
        packingString = inString + ';' + targetWeight + ';' + targetWeight
        return packing(packingString)
    
def testPartition():
    testvals = [
        ('', ''),
        ('5', 'no'),
        ('5 7', 'no'),
        ('6 6', '6'),
        ('6 6 7 7', '6 7'),
        ('3 3 3 3 1000 1000 1000 1000', '3 3 1000 1000'),
    ]

    for (inString, solution) in testvals:
        val = partition(inString)
        utils.tprint(inString,':', val)
        assert val == solution
        

