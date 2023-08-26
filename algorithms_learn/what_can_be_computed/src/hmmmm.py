# This program is used in an exercise in chapter 2.
import utils; from utils import rf
def hmmmm(inString):   
    m = int(inString)
    if m>0 and m%10==0:
        return 'yes'
    else:
        return 'no'    


def testHmmmm():
    testVals = [('0', 'no'),
                ('10', 'yes'),
                ('50', 'yes'),
                ('4523', 'no'),
                ('-200', 'no'),
                ]
    for (inString, solution) in testVals:
        val = hmmmm(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
