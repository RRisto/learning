# SISO program yesOnSelf.py

# This is an APPROXIMATE solution to the computational problem
# YesOnSelf, which is in fact uncomputable.

# progString: a Python program P

# returns: if this program did in fact solve YesOnSelf, it would
# return 'yes' if P(P) is 'yes', and 'no' otherwise. However, this is
# an approximate version that relies on simulating P(P), so it only
# returns in the cases where P halts on input P. See yesOnString.py
# for details.
import utils; from utils import rf
from yesOnString import yesOnString  
def yesOnSelf(progString):   
    return yesOnString(progString, progString) 


def testyesOnSelf():
    testvals = [
        ('containsGAGA.py', 'yes'),
        ('isEmpty.py', 'no'),
    ]
    for (filename, solution) in testvals:
        val = yesOnSelf(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution
