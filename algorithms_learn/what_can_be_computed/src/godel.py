# SISO program godel.py

# This program is constructed in such a way that it allows us to prove
# the existence of true unprovable statements; the program itself does
# not compute anything natural or useful. The program ignores its
# input and instead reads its own source code, converting it into a
# Peano arithmetic statement equivalent to the statement H = "this
# program doesn't halt." If H is provable, the program
# halts. Otherwise it runs forever.

import utils; from utils import rf
# The following import is NOT an oracle function. The function              
# provableInPeano correctly \emph{recognizes} provable strings, but does not
# decide them. See claim on page~\pageref{claim:ProvableInPeano}.
from provableInPeano import provableInPeano 

# The following import is a computable function---NOT an oracle.
# See page~\pageref{page:convertHaltToPeano.py}.
from convertHaltToPeano import convertHaltToPeano 

def godel(inString):
    godelProg = rf('godel.py') 
    haltInPeano = convertHaltToPeano(godelProg) 
    notHaltInPeano = 'NOT ' + haltInPeano 
    if provableInPeano(notHaltInPeano) == 'yes': 
        return 'halted' # any value would do 
    else: # This line will never be executed! But anyway...   
        utils.loop() # deliberate infinite loop       
    

def testGodel():
    # Since provableInPeano() and convertHaltToPeano() are not
    # implemented, there is nothing reasonable to assert in this
    # test. We just run the code.
    inString = 'asdf'
    val = utils.runWithTimeout(None, godel, inString)

