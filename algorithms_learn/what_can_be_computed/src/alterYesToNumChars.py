# SISO program alterYesToNumChars.py

# Given string encoding program P and input I, return 'xxx' if
# P(I)='yes' and otherwise return 'xx'. This allows us to distinguish
# P(I) based on the number of characters returned.

# inString: Encodes Python program P and an input I for P, encoded via
# utils.ESS()

# returns: 'xxx' if P(I)='yes' and otherwise 'xx'.

# Example:
# >>> alterYesToNumChars(utils.ESS(rf('containsGAGA.py'), 'TTGAGATT'))
# 'xxx'
import utils; from utils import rf
from universal import universal  
def alterYesToNumChars(inString):
    (progString, newInString) = utils.DESS(inString)
    val = universal(progString, newInString)
    if val == 'yes':
        # return a string with three characters
        return 'xxx'
    else:
        # return a string with two characters
        return 'xx'  

def testAlterYesToNumChars():
    for (progName, inString, solution) in [
            ('containsGAGA.py', 'GAGAGAGAG', 'xxx'), 
            ('containsGAGA.py', 'TTTTGGCCGGT', 'xx'),
    ]:
        val = alterYesToNumChars(utils.ESS(rf(progName), inString))
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

