# SISO program verifyAdd.py

# This program is used in the exercises of chapter 12.

# The parameters I, S, H are the instance, proposed solution, and hint
# for a verifier as described in Chapter 12.

# The return value is as described in Chapter 12 for verifiers:
# 'correct' if S was successfully verified, and 'unsure' otherwise.
import utils; from utils import rf
def verifyAdd(I, S, H):  
    if len(S)>2*len(I) or len(H)>0:
        return 'unsure'
    (M1, M2) = [int(x) for x in I.split()]
    S = int(S)
    total = M1
    for i in range(M2):
        total += 1
    if total == S:
        return 'correct'
    else:
        return 'unsure'  
        
    

def testverifyAdd():
    testVals = [('5 6', '11', 'xx', 'unsure'),
                ('5 6', '11', '', 'correct'),
                ('5 6', '10', '', 'unsure'),
                ]
    for (I, S, H, retVal) in testVals:
        val = verifyAdd(I, S, H)
        utils.tprint(I, S, H, ':', val)
        assert val == retVal
