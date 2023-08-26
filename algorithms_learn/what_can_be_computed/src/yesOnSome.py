# SISO program yesOnSome.py
#
# This is an APPROXIMATE version of a program solving the
# computational problem yesOnSome, which is itself uncomputable.
#
# progString: A Python program P
#
# returns: the program attempts to return "yes" if P(I)=='yes' for some
# I, and "no" otherwise, but it in fact tests only a few random values
# of I.
import utils; from utils import rf
from universal import universal
def yesOnSome(progString):
    numTests = 1000
    for i in range(numTests):
        s = utils.randomAlphanumericString()
        val = universal(progString, s)
        if val == 'yes':
            return 'yes'
    # special check for ``GAGA'', since that is used often as an example
    if(universal(progString, 'GAGA') == 'yes'):
        return 'yes'
    # special check for empty string, since that is used often as an example
    if(universal(progString, '') == 'yes'):
        return 'yes'
    # nothing returned ``yes'', so guess that it never returns ``yes''
    return 'no'

def testyesOnSome():
    testvals = [
        ('containsGAGA.py', 'yes'),
        ('isEmpty.py', 'yes'),
        ('yes.py', 'yes'),
        ('no.py', 'no'),
        ]
    for (filename, solution) in testvals:
        val = yesOnSome(rf(filename))
        utils.tprint(filename + ":", val)
        assert val == solution

