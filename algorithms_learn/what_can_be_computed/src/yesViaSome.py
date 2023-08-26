# SISO program yesViaSome.py

# Performs a reduction from YesOnString to YesOnSome.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function yesOnSome worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from yesOnSome import yesOnSome # oracle function  
def yesViaSome(progString, inString):
    utils.writeFile('progString.txt', progString)
    utils.writeFile('inString.txt', inString)
    return yesOnSome(rf('ignoreInput.py')) 

def testYesViaSome():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaSome(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

