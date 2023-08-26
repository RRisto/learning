# SISO program yesViaAll.py

# Performs a reduction from YesOnString to YesOnAll.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function yesOnAll worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from yesOnAll import yesOnAll # oracle function  
def yesViaAll(progString, inString):
    utils.writeFile('progString.txt', progString)
    utils.writeFile('inString.txt', inString)
    return yesOnAll(rf('ignoreInput.py')) 

def testYesViaAll():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaAll(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

