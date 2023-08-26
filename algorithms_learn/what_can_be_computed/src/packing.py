# SISO program packing.py

# Solves the computational problem Packing. Given an input which is a
# string representing a list of integer weights together with a low
# threshold L and high threshold H, it searches for a feasible packing
# i.e. a subset of the weights that sums to at least L and at most H.
# The recursive search algorithm enumerates all subsets of the weights
# and therefore requires exponential time in the worst case.

# inString: the integer weights are separated by whitespace from each
# other; L and H are separated from each other and from the weights by
# semicolons.

# returns: If a feasible packing exists, it is returned formatted as a
# sequence of weights separated by space characters. Otherwise 'no' is
# returned.

# Example:
# >>> packing('1 2 3000 4 5 6 7 8000 9; 10000 ; 15000')
# '3000 8000'
import utils; from utils import rf
def packing(inString):
    # Extract the weights and thresholds L, H
    (weightString, L, H) = inString.split(';')
    weights = [int(x) for x in weightString.split()]
    L = int(L); H = int(H)
    # Use a recursive strategy to search for a feasible packing.
    prefix = []
    prefixWeight = 0
    remainingWeights = weights
    aPacking = packingHelper(prefix, prefixWeight, remainingWeights, L, H)
    if aPacking == None:
        return 'no'
    else:
        weightStrings = [str(x) for x in aPacking]
        return ' '.join(weightStrings)

def packingHelper(prefix, prefixWeight, remainingWeights, L, H):
    """Helper function for recursively finding feasible packing.

    Args:

        prefix (list of int): list of integer weights that are already
            in the packing we are searching for

        prefixWeight (int): precomputed sum of the weights in prefix,
            passed as a parameter to prevent needless recomputation.

        remainingWeights (list of int): list of integer weights that
            are still available to be used in the packing we are
            searching for.

        L (int): the low threshold

        H (int): the high threshold

    Returns:

        list of int: A list P of integers that includes prefix and
            possibly some of remainingWeights, such that
            L<=sum(P)<=H. If no such list exists, None is returned.

    """
    
    if L<=prefixWeight and prefixWeight<=H:
        # We have found a feasible packing, so return it.
        return prefix
    elif len(remainingWeights)==0:
        # There is no feasible packing with this prefix, so return
        # None.
        return None
    else:
        # We don't have a solution yet, so we will attempt two recursive
        # calls to packingHelper(): the first one will not use the next
        # weight and the second one will use the next weight.
        newWeights = remainingWeights[1:]
        nextWeight = remainingWeights[0]
        # 1. Recursive call *without* the next weight
        aPacking = packingHelper(prefix, prefixWeight, newWeights, L, H)
        if aPacking!=None:
            return aPacking
        else:
            # 2. Recursive call *with* the next weight
            newPrefix = prefix + [nextWeight] # extends list
            newPrefixWeight = prefixWeight + nextWeight # adds numerical weights
            aPacking = packingHelper(newPrefix, newPrefixWeight, newWeights, L, H)
            return aPacking

def testPacking():
    testvals = [
        ('; 5; 5', 'no'),
        ('5 ; 5 ; 5 ', '5'),
        ('5 7; 5 ; 5 ', '5'),
        ('5 7; 7 ; 7 ', '7'),
        ('5 7; 6 ; 6 ', 'no'),
        ('5 7; 10 ; 15 ', '5 7'),
        ('1 2 3000 4 5 6 7 8000 9; 10000 ; 15000 ', '3000 8000'),
        ('1 2 3000 4 5 6 7 8000 9; 100 ; 150 ', 'no'),
    ]

    for (inString, solution) in testvals:
        val = packing(inString)
        utils.tprint(inString,':', val)
        assert val == solution
        

