# SISO program provableInPeano.py

# Determine whether a given statement in Peano Arithmetic is
# provable. If the imported function isPeanoProof() were fully
# implemented, then the code for provableInPeano() given below would
# recognize but not decide provable statements. However, the materials
# do not provide a full implementation of isPeanoProof(), so
# provableInPeano() only works for a single trivial case that can be
# used for testing purposes.

# inString: a statement S in Peano Arithmetic

# returns: If implemented correctly, this function would return 'yes'
# if S has a proof in Peano Arithmetic. Otherwise it would not
# terminate. However, as stated above, this implementation works
# correctly only for a single trivial case.

import utils; from utils import rf
# The following import is NOT an oracle---it's a computable function.  
from isPeanoProof import isPeanoProof 
def provableInPeano(inString):
    proofString = ''
    while True:
        if isPeanoProof(proofString, inString)=='yes': 
            return 'yes'
        proofString = utils.nextASCII(proofString) 

def testprovableInPeano():
    # isPeanoProof() works only for one particular string ('0=0') in our
    # artificial, skeletal implementation for testing purposes. So we test only that string.
    inString = '0=0'
    val = provableInPeano(inString)
    utils.tprint(inString, ':', val)
    assert val == 'yes'
