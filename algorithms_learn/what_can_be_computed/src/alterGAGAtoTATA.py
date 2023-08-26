# SISO program alterGAGAtoTATA.py

# Given string encoding program P and input I, return P(I) except
# 'GAGA' becomes 'TATA'.

# inString: Encodes Python program P and an input I for P, encoded via
# utils.ESS()

# returns: P(I), unless P(I)='GAGA' in which case 'TATA' is returned.

# Example:
# >>> alterGAGAtoTATA(utils.ESS(rf('repeatCAorGA.py'), 'GA'))
# 'TATA'
import utils; from utils import rf
from universal import universal  
def alterGAGAtoTATA(inString):
    (progString, newInString) = utils.DESS(inString) 
    val = universal(progString, newInString)  
    if val == 'GAGA': 
        return 'TATA'
    else:
        return val 

def testAlterGAGAtoTATA():
    testvals = [('repeatCAorGA.py', 'CA', 'CACA'),
                ('repeatCAorGA.py', 'GA', 'TATA'),
            ]
    for (progName, inString, solution) in testvals:
        val = alterGAGAtoTATA(utils.ESS(rf(progName), inString))
        utils.tprint(progName, ',', inString, ':', val)
        assert val == solution
    
