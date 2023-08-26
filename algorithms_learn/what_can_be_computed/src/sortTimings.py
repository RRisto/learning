# python file sortTimings.py

import utils; from utils import rf
import time
def sortTimings(maxTime = None):
    """Run experiment on time required for builtin Python sorted() function.

    Args:

        maxTime (float): an approximate bound on the amount of time,
            in seconds, that this function should run before
            returning. This is present mostly for testing purposes,
            but it could also be useful for getting partial results in
            a limited time.

    Returns:

        list of 2-tuples (n, t): in each tuple, n is the number of
            items sorted and t is the average time to sort n items, in
            seconds.

    """
    functionStartTime = time.clock()
    timings = [ ]
    minItems = 100000
    maxItems = 1000000
    numItemsList = [10**k for k in range(1,6)]
    numDigits = 20
    allRandomNums = [ ]
    for i in range(max(numItemsList)):
        allRandomNums.append( int(utils.randomDigitalString(numDigits)) )
    for numItems in numItemsList:
        if maxTime and time.clock() - functionStartTime > maxTime:
            return timings
        randomNums = allRandomNums[:numItems]
        start = time.clock()
        numIters = 10
        for i in range(numIters):
            sortedNums = sorted(randomNums)
        stop = time.clock()
        timePerSort = (stop - start) / numIters
        timings.append( (numItems, timePerSort) )
        print (numItems, timePerSort)
    return timings

def testSortTimings():
    val = utils.runWithTimeout(None, sortTimings, 5)
    utils.tprint(val)

