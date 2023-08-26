# SISO program yesViaNumChars.py

# Performs a reduction from YesOnString to NumCharsOnString.

# progString: a python program P

# inString: An input string I

# returns: if the oracle function numCharsOnString worked correctly, this
# program would return "yes" if P(I) is "yes", and "no" otherwise.
import utils; from utils import rf
from numCharsOnString import numCharsOnString # oracle function  
def yesViaNumChars(progString, inString):
    singleString = utils.ESS(progString, inString)
    val = numCharsOnString(rf('alterYesToNumChars.py'), \
                                  singleString)
    if val == '3':
        return 'yes'
    else:
        return 'no' 

def testYesViaNumChars():
    testvals = [
        ('containsGAGA.py', 'TTTTGAGATT', 'yes'),
        ('containsGAGA.py', 'TTTTGAGTT', 'no'),
        ('isEmpty.py', '', 'yes'),
        ('isEmpty.py', 'x', 'no'),
    ]
    for (filename, inString, solution) in testvals:
        val = yesViaNumChars(rf(filename), inString)
        utils.tprint(filename + ":", val)
        assert val == solution

