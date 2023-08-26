# SISO program countLinesPlus1.py

# Return one more than the number of lines in the input.

# inString: a string S

# returns: One more than the number of lines in S.
import utils; from utils import rf
def countLinesPlus1(inString):          
    # split on newlines
    lines = inString.split('\n')
    # return the number of lines, as a string
    return str(len(lines)+1)         


def testcountLinesPlus1():
    testVals = [('', '2'), 
                ('abc', '2'),
                ('abc\n', '3'),
                ('\n', '3'),
                ('abc\ndef', '3'),
                ('abc\ndef\nghi', '4'),
                ('abc\ndef\nghi\n', '5'),
                ]
    for (inString, solution) in testVals:
        val = countLinesPlus1(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
