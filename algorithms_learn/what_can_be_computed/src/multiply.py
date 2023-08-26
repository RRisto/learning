# SISO program multiply.py

# Computes the product of two integers provided as input.

# inString: a string consisting of two integers separated by whitespace.

# returns: The product of the input integers.
import utils; from utils import rf
def multiply(inString): 
    (M1, M2) = [int(x) for x in inString.split()] 
    product = M1 * M2 
    return str(product) 

def testMultiply():
    testVals = [('4 5', 4*5),
                ('100 10000', 100*10000),
                ('1024 256', 1024*256)]
    for (inString, solution) in testVals:
        val = multiply(inString)
        utils.tprint (inString, val)
        assert int(val) == solution

