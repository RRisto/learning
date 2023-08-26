# SISO program isEmpty.py

# Returns 'yes' if its input is the empty string and 'no' otherwise.
import utils; from utils import rf
def isEmpty(inString):
    if inString == '':
        return 'yes'
    else:
        return 'no'

def testisEmpty():
    testVals = [('', 'yes'),
                ('asdf', 'no'),
                ]
    for (inString, solution) in testVals:
        val = isEmpty(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
