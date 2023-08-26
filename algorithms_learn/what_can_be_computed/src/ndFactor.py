# SISO program ndFactor.py

# Solves the computational problem Factor nondeterministically. Given
# an input integer M, it returns a nontrivial factor of M, or 'no' if
# no such factor exists.

# inString: an integer M.

# returns: a nontrivial factor of M, or 'no' if no such factor
# exists. Because a nondeterministic algorithm is used, different
# factors could be returned on different runs with the same inputs.

# Example:
# >>> ndFactor('15')
# '3'
import utils; from utils import rf
from threading import Thread
import threading

# The main function calls the helper function ndFactorHelper with
# suitable parameters.
def ndFactor(inString):
    M = int(inString)
    low = 2
    high = M
    nonDetSolution = utils.NonDetSolution()
    ndFactorHelper(M, low, high, nonDetSolution)
    return nonDetSolution.getSolution()


# This helper function searches nondeterministically for a factor m of
# M in the range low<=m<high), storing any positive solution found in
# the given nonDetSolution.  The function uses a divide and conquer
# approach, splitting the given interval into two smaller intervals
# and launching new threads to search those intervals -- unless the
# interval already has size 1, in which case the only possible value
# of m is tested.
def ndFactorHelper(M, low, high, nonDetSolution):  
    if high <= low:
        # There is nothing to search.
        return
    elif high - low == 1:
        # The search interval includes only one possibility (low), so test it.
        if M%low==0:
            # low is a factor of M, so store this solution
            nonDetSolution.setSolution(str(low))
        return
    else:
        # Split the search interval in two, and launch new threads to
        # search those intervals.
        threads = [ ] 
        childNdSoln = utils.NonDetSolution() 
        mid = int( (high+low)/2 )
        t1 = Thread(target=ndFactorHelper, args = (M,low,mid,childNdSoln))
        t2 = Thread(target=ndFactorHelper, args = (M,mid,high,childNdSoln))
        threads.append(t1)
        threads.append(t2)
        solution = utils.waitForOnePosOrAllNeg(threads, childNdSoln)
        nonDetSolution.setSolution(solution)


def testNdFactor():
    for M in (1,2,3,4,5,10,15,36,37,49,97,121,0,-5):
        val = ndFactor(str(M))
        utils.tprint(M, ':', val)
        if M<2 or utils.isPrime(M):
            assert val == 'no'
        else:
            assert M % int(val) == 0

