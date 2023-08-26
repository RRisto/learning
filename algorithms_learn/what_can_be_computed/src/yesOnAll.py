# SISO program yesOnAll.py
#
# This is an APPROXIMATE version of a program solving the
# computational problem yesOnAll, which is itself uncomputable.
#
# progString: A Python program P
#
# returns: the program attempts to return "yes" if P(I)=='yes' for all
# I, and "no" otherwise, but it in fact tests only a few random values
# of I.
import utils; from utils import rf
from universal import universal
def yesOnAll(progString):
    numTests = 1000
    for i in range(numTests):
        s = utils.randomAlphanumericString()
        val = universal(progString, s)
        if val != 'yes':
            return 'no'
    return 'yes'

def testYesOnAll():
    testvals = [
        ('containsGAGA.py', 'no'),
        ('isEmpty.py', 'no'),
        ('yes.py', 'yes'),
        ]
    for (filename, solution) in testvals:
        val = yesOnAll(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution

