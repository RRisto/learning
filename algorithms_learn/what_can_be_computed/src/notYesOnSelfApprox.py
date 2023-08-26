# SISO program notYesOnSelfApprox.py

# This program approximates the desired behavior of notYesOnSelf.  It
# works correctly on certain values of progString.
import utils; from utils import rf
from yesOnSelfApprox import yesOnSelfApprox
def notYesOnSelfApprox(progString):   
    val = yesOnSelfApprox(progString)
    if (val == 'yes'):
        return 'no'
    elif (val == 'no'):
        return 'yes'
    else:
        return 'unknown' 


def testnotYesOnSelfApprox():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('longerThan1K.py', 'yes'),
        ('yes.py', 'no'),
    ]
    for (filename, solution) in testvals:
        val = notYesOnSelfApprox(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution
    
