# SISO program listEvens.py

# This program is used in the exercises for Chapter 10.

import utils; from utils import rf
# The input should be a positive integer M in decimal notation. This   
# program returns a list of all positive even integers less than M,
# separated by commas.
def listEvens(inString):
    M = int(inString)
    evens = [ ]
    for i in range(2,M):    
        if i % 2 == 0: 
            evens.append(str(i))
    return ','.join(evens) 

def testListEvens():
    testVals = [(1, ''),
                (2, ''),
                (3, '2'),
                (4, '2'),
                (5, '2,4'),
                (10, '2,4,6,8'),
                (15, '2,4,6,8,10,12,14'),
                ]
    for (M, solution) in testVals:
        val = listEvens(str(M))
        utils.tprint(M, ':', val)
        assert val == solution
        

