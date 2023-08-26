# SISO program haltsViaNumSteps.py

# Reduces the problem HaltsOnString to NumStepsOnString.

# progString: A Python program P

# inString: An input string I

# returns: If the article function numStepsOnString were implemented
# correctly (which is impossible) this program would return 'yes' if
# the computation of P(I) halts and otherwise return 'no'. 
import utils; from utils import rf
from numStepsOnString import numStepsOnString # oracle function  
def haltsViaNumSteps(progString, inString):
    val = numStepsOnString(progString, inString)
    if val == 'no':
        return 'no'
    else:
        return 'yes' 

def testHaltsViaNumSteps():
    # utils.TEST_TIMEOUT = 2.0 # exit infinite loop after two seconds
    for (progName, inString, solution) in [
            ('loopIfContainsGAGA.py', 'GAGAGAGAG', 'no'), \
            ('loopIfContainsGAGA.py', 'TTTTGGCCGGT', 'yes') ]:
        val = haltsViaNumSteps(rf(progName), inString)
        utils.tprint( (progName, inString), ":", val )
        assert val == solution

