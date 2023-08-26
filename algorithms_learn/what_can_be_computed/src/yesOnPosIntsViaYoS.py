# SISO program yesOnPosIntsViaYoS.py

# This program is NOT a correct reduction from YesOnPosInts to YesOnString.
# It is used as the basis for one of the exercises in the chapter on Turing
# reductions.

# progString: a python program P

# returns: if it worked correctly, this program would return "yes" if
# P(str(n)) is "yes" for all positive integers n, and "no" otherwise.
import utils; from utils import rf
from yesOnString import yesOnString  
def yesOnPosIntsViaYoS(progString):
    i = 1
    while True:
        if not yesOnString(progString, str(i))=='yes':
            return 'no'
        i += 1 

    
    
def testyesOnPosIntsViaYoS():
    testVals = [('containsGAGA.py', 'no'),
                ('yes.py', None),
                ]
    for (filename, solution) in testVals:
        inString = rf(filename)
        val = utils.runWithTimeout(None, yesOnPosIntsViaYoS, inString)
        utils.tprint(inString, ':', val)
        assert val == solution
