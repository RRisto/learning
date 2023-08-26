# SISO program weirdYesOnString.py

# This program is deliberately crafted to enable a certain proof by
# contradiction. Given input string progString representing a python
# program P, weirdYesOnString returns 'no' if P(P) is 'yes';
# otherwise, 'no' is returned.
import utils; from utils import rf
from yesOnString import yesOnString 
def weirdYesOnString(progString): 
    if yesOnString(progString, progString)=='yes': 
        return 'no' 
    else: 
        return 'yes' 



def testweirdYesOnString():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('isEmpty.py', 'yes'),
    ]
    for (filename, solution) in testvals:
        val = weirdYesOnString(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution
    
