# SISO program isOdd.py

# Returns 'yes' if the input is an odd integer and 'no' otherwise. An
# exception will be thrown if the input string does not represent an
# integer.
import utils; from utils import rf
def isOdd(inString): 
    if int(inString) % 2 == 1:
        return 'yes'
    else:
        return 'no' 

def testisOdd():
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
        val = isOdd(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
