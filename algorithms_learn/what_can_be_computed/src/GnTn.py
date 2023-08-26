# SISO program GnTn.py

# Returns 'yes' if the input string is a member of the language GnTn,
# and 'no' otherwise. The language GnTn consists of strings consisting
# of n G's followed by n T's, for some n>=0.

# Example:
# >>> GnTn('GGGGTTTT')
# 'yes'
import utils; from utils import rf
def GnTn(inString): 
    length = len(inString)
    # length must be even
    if length % 2 != 0: return 'no'
    # split into first half and second half of input
    firstHalf = inString[:length//2]
    secondHalf = inString[length//2:]
    # firstHalf must contain all Gs
    for x in firstHalf:
        if x != 'G': return 'no'
    # secondHalf must contain all Ts
    for x in secondHalf:
        if x != 'T': return 'no'
    return 'yes' 

def testGnTn():
    testvals = [('', 'yes'),
                ('GT', 'yes'),
                ('GGTT', 'yes'),
                ('GGGTTT', 'yes'),
                ('GGGGTTTT', 'yes'),
                ('G', 'no'),
                ('T', 'no'),
                ('TG', 'no'),
                ('GGTTT', 'no'),
                ('TTTTTT', 'no'),
                ('GGTTTT', 'no'),
            ]
    for (inString, solution) in testvals:
        val = GnTn(inString)
        utils.tprint(inString, ': ', val)
        assert val == solution


