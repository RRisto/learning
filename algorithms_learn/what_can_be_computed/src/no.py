# SISO program no.py

# Returns 'no' for all inputs.
import utils; from utils import rf
def no(inString):
    return 'no'


def testNo():
    testVals = [('', 'no'),
                ('x', 'no'),
                ('asdf', 'no'),
                ('GAGAGAGAGAGA', 'no'),
                ]
    for (inString, solution) in testVals:
        val = no(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
