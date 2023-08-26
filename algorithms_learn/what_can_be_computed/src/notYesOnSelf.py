# SISO program notYesOnSelf.py

# This is an APPROXIMATE solution to the computational problem
# NotYesOnSelf, which is in fact uncomputable.

# progString: a Python program P

# returns: if this program did in fact solve NotYesOnSelf, it would
# return 'yes' if P(P) is not 'yes', and 'no' otherwise. However, this
# is an approximate version that relies on simulating P(P), so it only
# returns in the cases where P halts on input P. See yesOnString.py
# and yesOnSelf.py for details.
import utils; from utils import rf
from yesOnSelf import yesOnSelf
def notYesOnSelf(progString):   
    val = yesOnSelf(progString)
    if val == 'yes':
        return 'no'
    else:
        return 'yes' 


def testNotYesOnSelf():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('isEmpty.py', 'yes'),
    ]
    for (filename, solution) in testvals:
        val = notYesOnSelf(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution
    
