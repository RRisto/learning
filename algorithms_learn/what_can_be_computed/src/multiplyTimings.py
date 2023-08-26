import utils; from utils import rf
import time
def multiplyTimings(maxTime = None):
    """Conduct experiment on the amount of time required for multiplication.

    This function can be used to conduct experiments on the amount of
    time required to compute multiplications of very large numbers,
    producing results similar to those discussed in Chapter 10.

    Args:

        maxTime (float): an approximate bound on the amount of time,
            in seconds, that this function should run before
            returning. This is present mostly for testing purposes,
            but it could also be useful for getting partial results in
            a limited time.

    Returns:

        list of 2-tuples (numDigits, timePerMult) containing (int,
            float): In each element of the list, numDigits is the
            number of digits in each of the two numbers that were
            multiplied together, and timePerMult is the time required
            to perform such a multiplication, in seconds. In fact,
            many multiplications of random numbers of the required
            length are performed and the time required is the average
            of these.

    """
    
    functionStartTime = time.clock()
    timings = [ ]
    minDigits = 500
    maxDigits = 10000
    for numDigits in range(minDigits, maxDigits + minDigits, minDigits):
        if maxTime and time.clock() - functionStartTime > maxTime:
            return timings
        numRandomPairs = 1000
        randomPairs = [ ]
        for i in range(numRandomPairs):
            num1 = int(utils.randomDigitalString(numDigits))
            num2 = int(utils.randomDigitalString(numDigits))
            randomPairs.append( (num1,num2) )
        start = time.clock()
        numIters = 10
        for i in range(numIters):
            for (num1,num2) in randomPairs:
                val = num1 * num2
        stop = time.clock()
        timePerMult = (stop - start) / (numIters * numRandomPairs)
        timings.append( (numDigits, timePerMult) )
        # print (numDigits, timePerMult)
    return timings

def testMultiplyTimings():
    val = utils.runWithTimeout(None, multiplyTimings, 5)
    utils.tprint(val)

