# SISO program isEven.py

# Returns 'yes' if the last character of the input is an even digit
# and 'no' otherwise.
import utils; from utils import rf
def lastDigitIsEven(inString): 
    lastDigit = inString[-1] # ``[-1]'' is Python notation for last element
    if lastDigit in '02468':
        return 'yes'
    else:
        return 'no' 

def testlastDigitIsEven():
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
        val = lastDigitIsEven(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
    
    
