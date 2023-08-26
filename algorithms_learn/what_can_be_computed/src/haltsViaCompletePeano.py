# SISO program haltsViaCompletePeano.py

# Solves the problem HaltsOnEmpty, assuming that Peano arithmetic is
# complete. (In fact, this proves that Peano arithmetic is incomplete,
# since otherwise the program below would contradict the
# undecidability of the halting problem.)

# inString: a Python program P

# returns: If Peano arithmetic were complete (which it is not) this
# program would return 'yes' if the computation of P('') halts and
# otherwise return 'no'.

# Note that the program imports two unimplemented functions,
# isPeanoProof() and convertHaltToPeano(). These are indeed computable
# functions and could be implemented in Python, but their
# implementations would be long and tedious and are not provided.

import utils; from utils import rf
# The following two imports are computable functions, NOT oracles.  
from isPeanoProof import isPeanoProof 
from convertHaltToPeano import convertHaltToPeano

def haltsViaCompletePeano(inString):
    haltInPeano = convertHaltToPeano(inString) 
    notHaltInPeano = 'NOT ' + haltInPeano 
    proofString = ''
    while True:
        if isPeanoProof(proofString, haltInPeano)=='yes': 
            return 'yes'
        if isPeanoProof(proofString, notHaltInPeano)=='yes': 
            return 'no'
        proofString = utils.nextASCII(proofString)  

def testhaltsViaCompletePeano():
    # Since isPeanoProof() and convertHaltToPeano() are not
    # implemented, there is nothing reasonable to assert in this
    # test. We just run the code.
    inString = 'asdf'
    val = utils.runWithTimeout(None, haltsViaCompletePeano, inString)
        
