# SISO program GAGAOnString.py
#
# This is an APPROXIMATE version of a program solving the
# computational problem GAGAOnString, which is itself uncomputable.
#
# progString: A Python program P
#
# inString: A string I, to be thought of as an input to P
#
# returns: the program attempts to return "yes" if P(I)=='GAGA' and "no"
# otherwise, but it will fail if its simulation of P enters an
# infinite loop.
import utils; from utils import rf
from universal import universal
def GAGAOnString(progString, inString):
    val = universal(progString, inString)
    if val == 'GAGA':
        return 'yes'
    else:
        return 'no'

def testGAGAOnString():
    testvals = [('containsGAGA.py', 'GAGAGAGAG', 'no'), 
                ('repeatCAorGA.py', 'CA', 'no'), 
                ('repeatCAorGA.py', 'GA', 'yes') ]
    for (progName, inString, solution) in testvals:
        val = GAGAOnString(rf(progName), inString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

