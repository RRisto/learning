# SISO program weirdCountLines.py

# This program is used in the exercises of chapter 3.
import utils; from utils import rf
from countLines import countLines   
from countLinesPlus1 import countLinesPlus1
def weirdCountLines(inString):          
    if inString == rf('weirdCountLines.py'):
        return countLinesPlus1(inString)
    else:
        return countLines(inString)  


def testweirdCountLines():
    testVals = [(rf('weirdCountLines.py'), '24'),
                ('asdf', '1'),
                ]
    for (inString, solution) in testVals:
        val = weirdCountLines(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

