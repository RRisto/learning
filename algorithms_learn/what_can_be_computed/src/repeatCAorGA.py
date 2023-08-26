# SISO program repeatCAorGA.py

# This simple function is used in the book to illustrate
# program-altering programs. If the input is 'CA', then 'CACA' is
# returned. If the input is 'GA', then 'GAGA' is returned. For all
# other inputs, 'unknown' is returned.
import utils; from utils import rf
def repeatCAorGA(inString):  
    if inString == 'CA':
        return 'CACA'
    elif inString == 'GA':
        return 'GAGA'
    else:
        return 'unknown'  


def testrepeatCAorGA():
    testVals = [('CA', 'CACA'),
                ('GA', 'GAGA'),
                ('CCCCTTTAA', 'unknown'),
                ]
    for (inString, solution) in testVals:
        val = repeatCAorGA(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
