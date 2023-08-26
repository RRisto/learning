# SISO program containsGAGA.py

# Return 'yes' if the input contains the substring 'GAGA'. Otherwise return 'no'.

# inString: the string to be searched

# returns: 'yes' if the input contains 'GAGA'. Otherwise return 'no'

# Example:
# >>> containsGAGA('CCCCCCGAGATTTATA')
# 'yes'
import utils; from utils import rf   
def containsGAGA(inString): 
    if 'GAGA' in inString: 
        return 'yes' 
    else: 
        return 'no' 


# Most of the Python files provided with WCBC contain one or more test
# functions. If you're not familiar with Python, ignore these test
# functions until you have more experience. Once you know more Python,
# you can read the test functions to see examples of the expected
# behavior of the main function, and you can invoke test functions to
# check the correctness of the main function.
def testContainsGAGA():
    testVals = [('GAGA', 'yes'),
                ('CCCGAGA', 'yes'),
                ('AGAGAGAAGAAGAGAAA', 'yes'),
                ('GAGACCCCC', 'yes'),
                ('', 'no'),
                ('CCCCCCCCGAGTTTT', 'no'),
                ]
    for (inString, solution) in testVals:
        val = containsGAGA(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
