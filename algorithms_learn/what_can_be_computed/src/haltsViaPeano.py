# SISO program haltsViaPeano.py

# Reduces HaltsOnEmpty to TrueInPeano. (In fact, this proves that
# Peano arithmetic is undecidable, since otherwise the program below
# would contradict the undecidability of the halting problem.)

# inString: a Python program P

# returns: If Peano arithmetic were decidable (which it is not) this
# program would return 'yes' if the computation of P('') halts and
# otherwise return 'no'.

# Note that the program imports the unimplemented function
# convertHaltToPeano(). This is indeed a computable function and
# could be implemented in Python, but its implementation would be
# long and tedious and is not provided.

import utils; from utils import rf
from trueInPeano import trueInPeano # oracle function  

# The following import is NOT an oracle---it's a computable function.
# See page~\pageref{page:convertHaltToPeano.py}.
from convertHaltToPeano import convertHaltToPeano 

def haltsViaPeano(inString):
    haltInPA = convertHaltToPeano(inString)
    return trueInPeano(haltInPA)  


def testhaltsViaPeano():
    # Since trueInPeano() is an oracle function that could never be
    # implemented, there is nothing reasonable to assert in this
    # test. We just run the code.
    inString = 'asdf'
    val = haltsViaPeano(inString)
    utils.tprint(inString, ':', val)
    
