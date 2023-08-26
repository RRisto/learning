# SISO program ignoreInput.py

# This program ignores its input parameter, instead executing a fixed
# pre-prepared computation based on a Python program and input string
# that have been stored on disk. The Python program P is stored in the
# file progString.txt and the input string I is stored in the file
# inString.txt.

# inString: The input parameter which is ignored.

# returns: P(I), where P and I are as described above.

# Example:
# >>> utils.writeFile('progString.txt', rf('containsGAGA.py'))
# >>> utils.writeFile('inString.txt', 'TTTGAGATT')
# >>> ignoreInput('CCCCCCC')
# 'yes'
import utils; from utils import rf
from universal import universal
def ignoreInput(inString): 
    progString = rf('progString.txt') 
    newInString = rf('inString.txt') 
    return universal(progString, newInString) 

def testIgnoreInput():
    for (progName, inString, solution) in [
            ('containsGAGA.py', 'GAGAGAGAG', 'yes'), \
            ('containsGAGA.py', 'TTTTGGCCGGT', 'no') ]:
        utils.writeFile('progString.txt', rf(progName))
        utils.writeFile('inString.txt', inString)
        val = ignoreInput('irrelevant input')
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

