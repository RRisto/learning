# SISO program alterYesToGAGA.py

# Given string encoding program P and input I, return 'GAGA' if
# P(I)='yes' and otherwise return 'no'.

# inString: Encodes Python program P and an input I for P, encoded via
# utils.ESS()

# returns: 'GAGA' if P(I)='yes' and otherwise 'no'.

# Example:
# >>> alterYesToGAGA(utils.ESS(rf('containsGAGA.py'), 'TTGAGATT'))
# 'GAGA'
import utils; from utils import rf
from universal import universal
def alterYesToGAGA(inString):  
    (progString, newInString) = utils.DESS(inString)
    val = universal(progString, newInString)
    if val == 'yes':
        return 'GAGA'
    else:
        return 'no'  

def testAlterYesToGAGA():
    for (progName, inString, solution) in [('containsGAGA.py', 'GAGAGAGAG', 'GAGA'), 
                                           ('containsGAGA.py', 'ATATACCC', 'no') ]:
        progString = rf(progName)
        combinedString = utils.ESS(progString, inString) 
        val = alterYesToGAGA(combinedString)
        utils.tprint( (progName, inString), ":", val )  
        assert val == solution


