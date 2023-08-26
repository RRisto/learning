# SISO program maybeLoop.py

# This program is used as an example of a decision program in chapter
# 3. If the input does not contain the string "secret sauce", the
# program enters an infinite loop. Otherwise, the output depends on
# the length L of the input. If L is even, 'yes' is returned,
# otherwise 'no' is returned.
import utils; from utils import rf
def maybeLoop(inString): 
    if not 'secret sauce' in inString:
        # enter an infinite loop
        i = 0
        while i>=0:
            i = i + 1
    else:
        # output ``yes'' if input length is even and ``no'' otherwise
        if len(inString) % 2 == 0:
            return 'yes'
        else:
            return 'no' 


def testmaybeLoop():
    testVals = [('', None),
                ('sdfjkhask', None),
                ('secret sauce', 'yes'),
                ('xsecret sauce', 'no'),
                ('xsecret saucex', 'yes'),
                ]
    for (inString, solution) in testVals:
        val = utils.runWithTimeout(None, maybeLoop, inString)
        utils.tprint(inString, ':', val)
        assert val == solution
        
