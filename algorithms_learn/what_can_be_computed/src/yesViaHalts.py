# SISO program yesViaHalts.py

# Performs a reduction from YesOnString to HaltsOnString.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function haltsOnString worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from haltsOnString import haltsOnString # oracle function  
def yesViaHalts(progString, inString):
    singleStr = utils.ESS(progString, inString)
    return haltsOnString(rf('alterYesToHalt.py'), singleStr) 

def testYesViaHalts():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaHalts(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

