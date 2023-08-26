# SISO program multiplyAll_documented.py [This file is essentially
# identical to multiplyAll.py, except that it contains documentation
# and tests. The file multiplyAll.py does not contain documentation or
# tests so that it can be used as input for certain examples in the
# textbook without creating unnecessary confusion.]

# Computes the product of some integers provided as input.

# inString: a string consisting of integers separated by whitespace.

# returns: The product of the input integers.
import utils; from utils import rf
def multiplyAll_documented(inString): 
    # split on whitespace 
    numbers = inString.split()  

    # convert strings to integers
    for i in range(len(numbers)):  
        numbers[i] = int(numbers[i]) 

    # compute the product of the numbers array
    product = 1  
    for num in numbers: 
        product = product * num   
        
    # convert the product to a string, and return it
    productString = str(product) 
    return productString 

def testmultiplyAll_documented():
    testVals = [('', '1'),
                ('1', '1'),
                ('2', '2'),
                ('1 5', '5'),
                ('2 5', '10'),
                ('10 20 30', '6000'),
                ('10 10 10 10 10 10 10 10 10 10', '10000000000'),
                ]
    for (inString, solution) in testVals:
        val = multiplyAll_documented(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
        
