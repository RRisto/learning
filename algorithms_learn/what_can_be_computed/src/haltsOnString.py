# SISO program haltsOnString.py

# Solves the computational problem haltsOnString, but only in an
# approximate fashion since the problem is known to be undecidable.

# progString: A Python program P

# inString: An input string I

# returns: If implemented correctly (which is impossible) this program
# would return 'yes' if the computation of P(I) halts and otherwise
# return 'no'. In practice, an approximate version of this is
# implemented: return 'yes' if the computation of P(I) halts before a
# fixed timeout, and otherwise return 'no'.

# Example:
# >>> haltsOnString(rf('containsGAGA.py'), 'TTTTTTTT')
# 'yes'
import utils; from utils import rf
from universal import universal
def haltsOnString(progString, inString):
    # if it doesn't complete before timing out, assume it is in an infinite loop
    val = utils.runWithTimeout(None, universal, progString, inString)
    if val != None:
        return 'yes'
    else:
        return 'no'


def testhaltsOnString():
    for (progName, inString, solution) in [
            ('loopIfContainsGAGA.py', 'GAGAGAGAG', 'no'), \
            ('loopIfContainsGAGA.py', 'TTTTGGCCGGT', 'yes') ]:
        val = haltsOnString(rf(progName), inString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution
    
