# SISO program MCopiesOfC.py

# inString: string representing an integer M. An exception will be
# raised if inString does not represent an integer.

# returns: a string consisting of M copies of the character 'C'.

# example:
# >>> MCopiesOfC('12')
# 'CCCCCCCCCCCC'
import utils; from utils import rf
def MCopiesOfC(inString):      
    M = int(inString)
    cList = [ ] 
    # iterate M times, appending a single ``C'' character at each iteration
    for i in range(M):
        cList.append('C') 
    # join all the C's together into a single string, with no separator
    return ''.join(cList) 

def testMCopiesOfC():
    testvals = [('0', ''),
                ('1', 'C'),
                ('2', 'CC'),
                ('20', 'CCCCCCCCCCCCCCCCCCCC'),
            ]
    for (inString, solution) in testvals:
        val = MCopiesOfC(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

