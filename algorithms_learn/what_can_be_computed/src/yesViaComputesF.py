# SISO program yesViaComputesF.py

# Performs a reduction from YesOnString to ComputesF.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function computesF worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from computesF import computesF # oracle function 
def yesViaComputesF(progString, inString):
    utils.writeFile('progString.txt', progString) 
    utils.writeFile('inString.txt', inString) 
    val = computesF(rf('alterYesToComputesF.py')) 
    if val == 'yes':
        return 'yes'
    else:
        return 'no' 

def testYesViaComputesF():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaComputesF(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution
