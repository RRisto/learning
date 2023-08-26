# SISO program yesOnString.py

# This is an APPROXIMATE solution to the computational problem
# YesOnString, which is in fact uncomputable.

# progString: a Python program P

# inString: an input string I

# returns: if this program did in fact solve YesOnString, it would
# return 'yes' if P(I) is 'yes', and 'no' otherwise. However, this is
# an approximate version that relies on simulating P(I), so it only
# returns in the cases where P halts on input I.
import utils; from utils import rf
from universal import universal
def yesOnString(progString, inString):
    val = universal(progString, inString)
    if val == 'yes':
        return 'yes'
    else:
        return 'no'

def testyesOnString():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesOnString(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution
