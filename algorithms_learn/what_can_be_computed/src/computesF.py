# SISO program computesF.py

# This is an APPROXIMATE version of solving the computational problem
# computesF, which is itself an uncomputable problem. Given a program
# P, we attempt to return 'yes' if P computes a particular predefined
# function F, and 'no' otherwise.

# progString: A Python program P.

# returns: 'yes' if P appears to compute a particular predefined
# function F (based on some random sampling of inputs and outputs),
# and 'no' otherwise.

# Example:
# >>> computesF(rf('containsGAGA.py'))
# 'no'
import utils; from utils import rf
from universal import universal
def computesF(progString):
    from F import F
    iters = 100
    for i in range(iters):
        inString = utils.randomAlphanumericString()
        val = utils.runWithTimeout(None, universal, progString, inString)
        if val: # returned a value, so check if it's the correct one
            if val != F(inString):
                return 'no'
        else: # timed out -- assume infinite loop
            return 'no'
    return 'yes'

# use e.g. utils.TEST_TIMEOUT = 1.0 before calling
def testComputesF():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('loop.py', 'no'),
        ('F.py', 'yes'),
    ]
    for (progName, solution) in testvals:
        val = computesF(rf(progName))
        utils.tprint( progName, ":", val )
        assert val == solution

