# SISO program slow10thPower.py

# This program is used in an exercise in Chapter 10.

import utils; from utils import rf
# Input is a nonnegative integer M in decimal notation. Output is $M^{10}$. 
# We could compute this efficiently using the Python ** operator,
# but here we deliberately use a slow iterative method.
def slow10thPower(inString):
    M = int(inString)
    product = 1
    for i in range(10):        
        product = product * M  
    return str(product) 

def testSlow10thPower():
    for M in [0, 1, 2, 8, 10, 100]:
        val = slow10thPower(str(M))
        solution = str(M**10)
        utils.tprint(M, ":", val)
        assert val == solution        

