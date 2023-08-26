# SISO program G.py

# This function is a placeholder for a generic computable function G.
# This particular choice of G returns the first character of the input
# string.
import utils; from utils import rf
def G(inString):
    if len(inString) >= 1:
        return inString[0]
    else:
        return ''


def testG():
    testvals = [('', ''),
                ('x', 'x'),
                ('abcdef', 'a'),
    ]

    for (inString, solution) in testvals:
        val = G(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
