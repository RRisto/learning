# SISO program mysteryMultiply.py

# This program is used in one of the exercises of chapter 10.

import utils; from utils import rf
# This is a strange and useless program, but it is good for practicing 
# the skill of estimating time complexity. The input is assumed to
# be a positive integer M in decimal notation.
def mysteryMultiply(inString):
    # make M concatenated copies of the input 
    copiedInString = int(inString) * inString
    # convert to integer and perform the mystery multiply
    val = int(copiedInString)
    return str(val*val*val)   

def testMysteryMultiply():
    testVals = [(1, '1'),
                (10, '1030610152128364555636973757573696355453628211510060301000')]
    for (M, solution) in testVals:
        val = mysteryMultiply(str(M))
        utils.tprint(M, ':', val)
        assert val == solution

