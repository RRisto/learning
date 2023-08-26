# python file someTests.py

# As explained in the README.txt, Python programs in this software
# package usually include test functions in the same file as the
# program itself. However, in some cases, it is preferable for the
# test functions to be in a separate file. For example, the textbook
# uses several examples of applying the countLines.py program to other
# Python programs. For these programs, we want the number of lines
# displayed in the textbook to match the number of lines actually in
# the file. So we can't include test functions in those files --
# including test functions would add lines to the file that don't
# appear in the book's figures. Therefore, test functions for those
# files are included here instead.
import utils; from utils import rf

from multiplyAll import multiplyAll
def testmultiplyAll():
    testVals = [('', '1'),
                ('1', '1'),
                ('2', '2'),
                ('1 5', '5'),
                ('2 5', '10'),
                ('10 20 30', '6000'),
                ('10 10 10 10 10 10 10 10 10 10', '10000000000'),
                ]
    for (inString, solution) in testVals:
        val = multiplyAll(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

from countLines import countLines
def testcountLines():
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
        val = countLines(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
        
