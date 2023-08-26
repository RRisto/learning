# SISO program factor.py

# Solves the computational problem Factor. Given an input integer M,
# it returns the smallest nontrivial factor of M, or 'no' if no such
# factor exists. A naive exponential time algorithm is employed.

# inString: an integer M.

# returns: the smallest nontrivial factor of M, or 'no' if no such
# factor exists

# Example:
# >>> factor('15')
# '3'
import utils; from utils import rf
def factor(inString): 
    M = int(inString)
    for i in range(2,M): 
        if M % i == 0: 
            return str(i)
    return 'no'  

def testFactor():
    for M in (1,2,3,4,5,10,15,36,37,49,97,121,0,-5):
        val = factor(str(M))
        utils.tprint(M, ':', val)
        if M<2 or utils.isPrime(M):
            assert val == 'no'
        else:
            assert M % int(val) == 0
