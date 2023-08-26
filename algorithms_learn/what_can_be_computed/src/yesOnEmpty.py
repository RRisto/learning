# SISO program yesOnEmpty.py
#
# This is an APPROXIMATE version of a program solving the
# computational problem yesOnEmpty, which is itself uncomputable.
#
# progString: A Python program P
#
# returns: the program attempts to return "yes" if P('')=='yes', and
# "no" otherwise, but it will fail if its simulation of P doesn't
# terminate.
import utils; from utils import rf
from universal import universal
def yesOnEmpty(progString):
    val = universal(progString, '')
    if val == 'yes':
        return 'yes'
    else:
        return 'no'

def testYesOnEmpty():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('isEmpty.py', 'yes'),
        ('yes.py', 'yes'),
        ]
    for (filename, solution) in testvals:
        val = yesOnEmpty(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution

