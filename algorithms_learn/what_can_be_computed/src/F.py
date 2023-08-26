# SISO program F.py

# This function is a placeholder for a generic computable function F.
# This particular choice of F returns the length of the input string.
import utils; from utils import rf
def F(inString):
    return str(len(inString))

def testF():
    testvals = [('', '0'),
                ('x', '1'),
                ('abcdef', '6'),
    ]

    for (inString, solution) in testvals:
        val = F(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

