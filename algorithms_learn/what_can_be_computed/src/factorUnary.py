# SISO program factorUnary.py

# Solves the computational problem FactorUnary. Given an input
# consisting of M 1's, it returns the smallest nontrivial factor of M,
# or 'no' if no such factor exists. A naive exponential time algorithm
# is employed.

# inString: a string consisting of M 1's.

# returns: the smallest nontrivial factor of M, or 'no' if no such
# factor exists

# Example:
# >>> factorUnary('111111111111111')
# '3'
import utils; from utils import rf
from factor import factor
def factorUnary(inString):
    M = len(inString)
    return factor(str(M))




def testFactorUnary():
    for M in (1,2,3,4,5,10,15,36,37,49,97,121):
        unaryM = '1'*M
        val = factorUnary(unaryM)
        utils.tprint(M, ':', val)
        if utils.isPrime(M):
            assert val == 'no'
        else:
            assert M % int(val) == 0

        
