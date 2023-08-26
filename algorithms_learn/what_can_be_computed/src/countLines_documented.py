# SISO program countLines_documented.py [This file is essentially
# identical to countLines.py, except that it contains documentation
# and tests. The file countLines.py does not contain documentation or
# tests so that it can be used as input for certain examples in the
# textbook without creating unnecessary confusion.]

# Return the number of lines in the input.

# inString: a string S

# returns: The number of lines in S.
import utils; from utils import rf
def countLines_documented(inString):          
    # split on newlines
    lines = inString.split('\n')
    # return the number of lines, as a string
    return str(len(lines))         


def testcountLines_documented():
    testVals = [('', '1'), # It is weird for the empty string to
                           # contain one line, but this is what the
                           # simple implementation above returns, and
                           # it's best to keep the simplest possible
                           # implementation for this tutorial example.
                ('abc', '1'),
                ('abc\n', '2'),
                ('\n', '2'),
                ('abc\ndef', '2'),
                ('abc\ndef\nghi', '3'),
                ('abc\ndef\nghi\n', '4'),
                ]
    for (inString, solution) in testVals:
        val = countLines_documented(inString)
        utils.tprint(inString, ':', val)
        assert val == solution


