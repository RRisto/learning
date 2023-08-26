# SISO program alterGAGAtoTATA2.py

# Given program P and input I, return P(I) except 'GAGA' becomes 'TATA'.

# progString: A Python program P.
# inString: An input I for the Python program

# returns: P(I), unless P(I)='GAGA' in which case 'TATA' is returned.

# Example:
# >>> alterGAGAtoTATA2(rf('repeatCAorGA.py'), 'GA')
# 'TATA'
import utils; from utils import rf
from alterGAGAtoTATA import alterGAGAtoTATA
def alterGAGAtoTATA2(progString, inString):
    singleString = utils.ESS(progString, inString)
    return alterGAGAtoTATA(singleString)

def testAlterGAGAtoTATA2():
    testvals = [('repeatCAorGA.py', 'CA', 'CACA'),
                ('repeatCAorGA.py', 'GA', 'TATA'),
            ]
    for (progName, inString, solution) in testvals:
        val = alterGAGAtoTATA2(rf(progName), inString)
        utils.tprint(progName, ',', inString, ':', val)
        assert val == solution


