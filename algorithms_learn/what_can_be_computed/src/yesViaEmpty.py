# SISO program yesViaEmpty.py

# Performs a reduction from YesOnString to YesOnEmpty.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function yesOnEmpty worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from yesOnEmpty import yesOnEmpty # oracle function  
def yesViaEmpty(progString, inString):
    utils.writeFile('progString.txt', progString)
    utils.writeFile('inString.txt', inString)
    return yesOnEmpty(rf('ignoreInput.py')) 

def testYesViaEmpty():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaEmpty(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

