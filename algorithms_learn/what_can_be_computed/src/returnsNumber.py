# file returnsNumber.py

# This is an example of a non-SISO program, as discussed in Chapter 2.
import utils; from utils import rf
def returnsNumber(inString): 
    return 32 


def testreturnsNumber():
    testVals = [('', 32),
                ('asdf', 32),
                ]
    for (inString, solution) in testVals:
        val = returnsNumber(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
