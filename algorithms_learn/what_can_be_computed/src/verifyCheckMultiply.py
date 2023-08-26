# SISO program verifyCheckMultiply.py

# This program is used in the exercises of chapter 12.  Note that it
# is *not* a correct implementation of a verifier for
# CheckMultiply. This program contains a deliberate mistake for use in
# one of the book's exercises.

# The parameters I, S, H are the instance, proposed solution, and hint
# for a verifier as described in Chapter 12.

# If implemented correctly, the return value would be as described in
# Chapter 12 for verifiers: 'correct' if S was successfully verified,
# and 'unsure' otherwise.
import utils; from utils import rf
def verifyCheckMultiply(I, S, H): 
    (M1, M2, K) = [int(x) for x in I.split()]
    if M1*M2==K and S=='yes':
        return 'correct'
    elif M1*M2!=K and S=='no':
        return 'correct'  
    else:
        return 'unsure' 


def testverifyCheckMultiply():
    testVals = [('5 6 30', 'yes', '', 'correct'),
                ('5 6 31', 'no', '', 'correct'),
                ('5 6 30', 'no', '', 'unsure'),
                ('5 6 31', 'yes', '', 'unsure'),
                ]
    for (I, S, H, retVal) in testVals:
        val = verifyCheckMultiply(I, S, H)
        utils.tprint(I, S, H, ':', val)
        assert val == retVal
    
