# Python file throwsException.py

# This file is used as an example in section 2.4.
import utils; from utils import rf
def throwsException(inString): 
    return 5 / 0 


def testthrowsException():
    testVals = ['', 'asdf']
    for inString in testVals:
        val = None
        try:
            val = throwsException(inString)
        except ZeroDivisionError:
            utils.tprint(inString, ':', val)
        else:
            # We should never get here, because an exception should
            # have been raised.
            assert False
        
