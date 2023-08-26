# SISO program isEven.py

# Returns 'yes' if the input is an even integer and 'no' otherwise. An
# exception will be thrown if the input string does not represent an
# integer.
import utils; from utils import rf
def isEven(inString):
    if int(inString) % 2 == 0:
        return 'yes'
    else:
        return 'no'

def testisEven():
    testVals = [('-2', 'yes'),
                ('0', 'yes'),
                ('2', 'yes'),
                ('3742788', 'yes'),
                ('-1', 'no'),
                ('1', 'no'),
                ('3', 'no'),
                ('17', 'no'),
                ('3953969', 'no'),
                ]
    for (inString, solution) in testVals:
        val = isEven(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
    
