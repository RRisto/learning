# SISO program isOddViaReduction.py

# Returns 'yes' if the input is an odd integer and 'no' otherwise,
# computing the solution via a reduction to the problem
# LastDigitIsEven. An exception will be thrown if the input string
# does not represent an integer.
import utils; from utils import rf
from lastDigitIsEven import lastDigitIsEven 
def isOddViaReduction(inString):
    inStringPlusOne = int(inString) + 1
    return lastDigitIsEven(str(inStringPlusOne)) 


def testisOddViaReduction():
    testVals = [('-2', 'no'),
                ('0', 'no'),
                ('2', 'no'),
                ('3742788', 'no'),
                ('-1', 'yes'),
                ('1', 'yes'),
                ('3', 'yes'),
                ('17', 'yes'),
                ('3953969', 'yes'),
                ]
    for (inString, solution) in testVals:
        val = isOddViaReduction(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
