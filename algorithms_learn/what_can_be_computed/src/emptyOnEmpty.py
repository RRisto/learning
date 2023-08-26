# SISO program emptyOnEmpty.py
#
# This is an APPROXIMATE version of a program solving the
# computational problem emptyOnEmpty, which is itself uncomputable.
#
# progString: A Python program P
#
# returns: the program attempts to return "yes" if P('')=='' and "no"
# otherwise, but it will fail if its simulation of P enters an
# infinite loop.
import utils; from utils import rf
from universal import universal
def emptyOnEmpty(progString):
    val = universal(progString, '')
    if val == '':
        return 'yes'
    else:
        return 'no'

def testEmptyOnEmpty():
    testvals = [('containsGAGA.py', 'no'), 
                ('isEmpty.py', 'no'), 
                ('onlyZs.py', 'yes') ]
    for (progName, solution) in testvals:
        val = emptyOnEmpty(rf(progName))
        utils.tprint( progName, ":", val )
        assert val == solution

