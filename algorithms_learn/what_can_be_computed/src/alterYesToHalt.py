# SISO program alterYesToHalt.py

# Given string encoding program P and input I, return 'GAGA' if
# P(I)='yes' and otherwise return 'no'.

# inString: Encodes Python program P and an input I for P, encoded via
# utils.ESS()

# returns: 'halted' if P(I)='yes' and otherwise enters an infinite loop.

# Example:
# >>> alterYesToHalt(utils.ESS(rf('containsGAGA.py'), 'TTGAGATT'))
# 'halted'
import utils; from utils import rf
from universal import universal 
def alterYesToHalt(inString):
    (progString, newInString) = utils.DESS(inString)
    val = universal(progString, newInString)
    if val == 'yes':
        # return value is irrelevant, since returning any string halts
        return 'halted' 
    else:
        # deliberately enter infinite loop
        utils.loop()  

def testAlterYesToHalt():
    for (progName, inString, solution) in [
            ('containsGAGA.py', 'GAGAGAGAG', 'halted'),
            ('containsGAGA.py', 'TTTTGGCCGGT', None),
    ]:
        combinedString = utils.ESS(rf(progName), inString)
        val = utils.runWithTimeout(None, alterYesToHalt, combinedString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

