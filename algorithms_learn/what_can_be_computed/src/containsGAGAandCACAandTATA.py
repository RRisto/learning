# SISO program containsGAGAandCACAandTATA.py

# Return 'yes' if the input contains all three of the strings 'GAGA', 'CACA', 'TATA'. Otherwise return 'no'.

# inString: the string to be searched

# returns: 'yes' if the input contains all three of the strings
# 'GAGA', 'CACA', 'TATA'. Otherwise return 'no'

# Example:
# >>> containsGAGAandCACAandTATA('CCCCCCGAGATTTATA')
# 'no'
import utils; from utils import rf  
from containsGAGA import *  
def containsGAGAandCACAandTATA(inString):
    if containsGAGA(inString)=='yes' and \
                  containsCACA(inString) and \
                          containsTATA(inString): 
        return 'yes'
    else:
        return 'no'   

def containsCACA(searchString):
    return containsSubstring(searchString, 'CACA')

def containsTATA(searchString):
    return containsSubstring(searchString, 'TATA')

def containsSubstring(searchString, subString):
    if subString in searchString:
        return True
    else:
        return False 


def testcontainsGAGAandCACAandTATA():
    testVals = [('GAGACACATATA', 'yes'),
                ('CTATACCACACGAGA', 'yes'),
                ('AGAGAGAAGAAGAGAATATAACACA', 'yes'),
                ('', 'no'),
                ('CCCCCCCCGAGTTTT', 'no'),
                ('CCCACAGAGACCCCCGAGTTTT', 'no'),
                ('CCTATAGAGACCCCCGAGTTTT', 'no'),
                ('CCTATACACACCCCCGAGTTTT', 'no'),
                ]
    for (inString, solution) in testVals:
        val = containsGAGAandCACAandTATA(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
