# SISO program yesOnStringApprox.py

# This program approximates the desired behavior of yesOnString.  It
# works correctly for four particular values of progString, but
# returns "unknown" for all other values of progString. See the
# exercises of chapter 3 for details.
import utils; from utils import rf
from containsGAGA import *
from longerThan1K import *
from maybeLoop import *
from yes import *
def yesOnStringApprox(progString, inString):   
    if progString == rf('containsGAGA.py'):
        return containsGAGA(inString)
    elif progString == rf('longerThan1K.py'):
        return longerThan1K(inString)
    elif progString == rf('yes.py'):
        return yes(inString)
    elif progString == rf('maybeLoop.py'):
        if not 'secret sauce' in inString: 
            return 'no'
        else:
            return maybeLoop(inString)
    else:
        return 'unknown' 




def testyesOnStringApprox():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('longerThan1K.py', 1500*'x', 'yes'),
        ('longerThan1K.py', 'xyz', 'no'),
        ('yes.py', 'xyz', 'yes'),
        ('maybeLoop.py', '', 'no'),
        ('maybeLoop.py', 'asdfhjksd', 'no'),
        ('maybeLoop.py', 'secret sauce', 'yes'),
        ('maybeLoop.py', 'xsecret sauce', 'no'),
        ('maybeLoop.py', 'xsecret saucex', 'yes'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesOnStringApprox(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution
    
