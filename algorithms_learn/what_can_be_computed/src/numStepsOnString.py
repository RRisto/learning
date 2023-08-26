# SISO program yesOnString.py

# This is an APPROXIMATE solution to the computational problem
# NumStepsOnString, which is uncomputable. In fact, this program uses
# elapsed time as a very approximate measure of the number of
# ``steps'' in the execution of the program, so it's a very poor
# approximation, but still useful for certain types of testing.

# progString: a Python program P

# inString: an input string I

# returns: if this program did in fact solve NumCharsOnString, it
# would return the number of steps in the computation of P(I) if P(I)
# terminates, and 'no' otherwise. However, this is an approximate
# version that relies on simulating P(I), so it guesses whether P(I)
# terminates based on a fixed timeout. Moreover, as mentioned above,
# even when P(I) terminates this program returns the elapsed time and
# not the number of steps.
import utils; from utils import rf
import time
from universal import universal
def numStepsOnString(progString, inString):
    start = time.clock()
    # if it doesn't complete before timing out, assume it is in an infinite loop
    val = utils.runWithTimeout(None, universal, progString, inString)
    elapsed = time.clock() - start
    if val:
        return str(elapsed)
    else:
        return 'no'
    

def testNumStepsOnString():
    for (progName, inString, solution) in [
            ('loopIfContainsGAGA.py', 'GAGAGAGAG', 'no'), \
            ('loopIfContainsGAGA.py', 'TTTTGGCCGGT', 'num') ]:
        val = numStepsOnString(rf(progName), inString)
        utils.tprint( (progName, inString), ":", val )
        if solution == 'no':
            assert val == solution
        else:
            # check returned val is a number
            try:
                float(val)
            except ValueError:
                assert False

