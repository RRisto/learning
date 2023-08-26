# SISO program recognizeEvenLength.py

# This program recognizes, but does not decide, the language of
# strings of even length. Given an input of even length, it will
# return 'yes'. Otherwise, it enters an infinite loop.
import utils; from utils import rf
def recognizeEvenLength(inString): 
    i = 0
    while True:
        if len(inString) == i:
            return 'yes'
        else:
            i = i + 2 


def testrecognizeEvenLength():
    testVals = [('', 'yes'),
                ('xx', 'yes'),
                ('xxxx', 'yes'),
                (200*'x', 'yes'),
                ('x', None),
                ('xxx', None),
                (201*'x', None),
                ]
    for (inString, solution) in testVals:
        val = utils.runWithTimeout(None, recognizeEvenLength, inString)
        utils.tprint(inString, ':', val)
        assert val == solution
            
