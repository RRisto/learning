# SISO program verifyFactorPolytime.py

# Verifies a solution to the computational problem Factor, in
# polynomial time.

# The parameters I, S, H are the instance, proposed solution, and hint
# for a verifier as described in Chapter 12.

# The return value is as described in Chapter 12 for verifiers:
# 'correct' if S was successfully verified, and 'unsure' otherwise.
import utils; from utils import rf
def verifyFactorPolytime(I, S, H): 
    # reject excessively long solutions and hints
    if len(S) > len(I) or len(H) > len(I):  
        return 'unsure'
    # the remainder of the program is identical to verifyFactor.py
    # ... 
    if S == 'no': return 'unsure' 
    M = int(I); m = int(S)
    if m>=2 and m<M and M % m == 0: 
        # m is a nontrivial factor of M
        return 'correct'
    else:
        # m is not a nontrivial factor of M
        return 'unsure'

def testVerifyFactorPolytime():
    testVals = [
            ('20','4', '', 'correct'),
            ('20','12', '', 'unsure'),
            ('20','no', '', 'unsure'), 
            ('20','5', '', 'correct'),
            ('20','2', '', 'correct'),
            ('20','11', '', 'unsure'), 
            ('31','-5', '', 'unsure'),
            ('31','0', '', 'unsure'),
            ('31','1', '', 'unsure'), 
            ('31','2', '', 'unsure'),
            ('31','3', '', 'unsure'),
            ('31','no', '', 'unsure'),
            ('3','1111111', '', 'unsure'),
            ('6','3', '111111111', 'unsure'),
    ]
    for (inString, maybeSolution, hint, solution) in testVals:
        val = verifyFactorPolytime(inString, maybeSolution, hint)
        utils.tprint(inString, maybeSolution, hint, ':', val)
        assert val == solution


