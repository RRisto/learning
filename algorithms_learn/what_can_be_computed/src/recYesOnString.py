# SISO program recYesOnString.py

# This program recognizes, but does not decide, the decision problem
# YesOnString.

# inString: Encodes Python program P and an input I for P, encoded via
# utils.ESS()

# returns: If P(I) is 'yes', returns 'yes'. If P(I) terminates but
# does not return 'yes', then 'no' is returned. If P(I) enters an
# infinite loop, this program also enters an infinite loop.

# Example:
# >>> recYesOnString(utils.ESS(rf('containsGAGA.py'), 'GA'))
# 'no'
import utils; from utils import rf
from universal import universal  
def recYesOnString(inString):
    (progString, newInString) = utils.DESS(inString) 
    val = universal(progString, newInString)  
    if val == 'yes':
        return 'yes'
    else:
        return 'no'  

def testRecYesOnString():
    for (progName, inString, solution) in [('containsGAGA.py', 'GAGAGAGAG', 'yes'), \
                                 ('containsGAGA.py', 'TTTTGGCCGGT', 'no') ]:
        combinedString = utils.ESS(rf(progName), inString)
        val = recYesOnString(combinedString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

