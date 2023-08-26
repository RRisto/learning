# SISO program numCharsOnString.py

# This is an APPROXIMATE solution to the computational problem
# NumCharsOnString, which is in fact uncomputable.

# progString: a Python program P

# inString: an input string I

# returns: if this program did in fact solve NumCharsOnString, it
# would return the length of P(I) if P(I) terminates, and 'no'
# otherwise. However, this is an approximate version that relies on
# simulating P(I), so it only returns in the cases where P halts on
# input I.
import utils; from utils import rf
from universal import universal
def numCharsOnString(progString, inString):
    val = universal(progString, inString)
    return str(len(val))

def testnumCharsOnString():
    for (progName, inString, solution) in [('containsGAGA.py', 'GAGAGAGAG', '3'), \
                                 ('containsGAGA.py', 'TTTTGGCCGGT', '2') ]:
        val = numCharsOnString(rf(progName), inString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

