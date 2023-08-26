# SISO program H.py

# This function is a placeholder for the impossible program H,
# described in the proof of claim 11.6.  This program, if it existed,
# would solve HaltsInExpTime in polynomial time.

# progString: A Python program P

# inString: An input string I

# returns: If implemented correctly (which is impossible) this program
# would return 'yes' if the computation of P(I) halts in fewer than
# 2^len(I) instructions and otherwise return 'no'; AND it would always
# return in time bounded by some fixed polynomial. In fact, we could
# implement this program so that it always returns the correct answer,
# but we cannot always do it in polynomial time. For similar program
# that succeeds in doing this in exponential time, see
# haltExTuring.py. (But note that haltExTuring.py works with Turing
# machines and not Python programs.)

import utils; from utils import rf
def H(progString, inString):
    if progString==rf('containsGAGA.py'):
        return 'yes'
    elif progString==rf('factor.py'):
        return 'no'
    else:
        return 'unknown'

def testH():
    testvals = [('containsGAGA.py', 'TTTTTTTTTTTTTTT', 'yes'),
                ('factor.py', '91', 'no'),
                ('multiply.py', '5 9', 'unknown')]

    for (progString, inString, solution) in testvals:
        val = H(rf(progString), inString)
        utils.tprint(progString, ':', val)
        assert val == solution


