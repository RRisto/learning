# SISO program yes.py

# Returns 'yes' for all inputs.
import utils; from utils import rf
def yes(inString): 
    return 'yes'   


def testYes():
    testVals = [('', 'yes'),
                ('x', 'yes'),
                ('asdf', 'yes'),
                ('GAGAGAGAGAGA', 'yes'),
                ]
    for (inString, solution) in testVals:
        val = yes(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
