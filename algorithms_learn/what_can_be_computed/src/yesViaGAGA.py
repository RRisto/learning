# SISO program yesViaGAGA.py

# Performs a reduction from YesOnString to GAGAOnString.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function GAGAOnString worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from GAGAOnString import GAGAOnString # oracle function  
def yesViaGAGA(progString, inString):
    singleString = utils.ESS(progString, inString)
    return GAGAOnString(rf('alterYesToGAGA.py'), singleString) 
                                            

def testYesViaGAGA():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaGAGA(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

