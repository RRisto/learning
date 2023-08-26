# SISO program yesOnSelfApprox.py

# This program approximates the desired behavior of yesOnSelf.  It
# works correctly on certain values of progString. See the exercises
# of chapter 3 for details.
import utils; from utils import rf
from yesOnStringApprox import yesOnStringApprox 
def yesOnSelfApprox(progString):   
    return yesOnStringApprox(progString, progString) 


def testyesOnSelfApprox():
    testvals = [
        ('containsGAGA.py', 'yes'),
        ('longerThan1K.py', 'no'),
        ('yes.py', 'yes'),
    ]
    for (filename, solution) in testvals:
        val = yesOnSelfApprox(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution
    
