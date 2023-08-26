# SISO program loopIfContainsGAGA.py

# If the input contains the string 'GAGA', this program enters an
# infinite loop. Otherwise it returns 'halted'. This function is used
# for certain tests that involve infinite loops.
import utils; from utils import rf
def loopIfContainsGAGA(inString): 
    if 'GAGA' in inString: 
        utils.loop() # infinite loop
    else:
        return 'halted' 

def testloopIfContainsGAGA():
    haltVal = 'halted'
    loopVal = 'loop'
    testvals = [
        ('', haltVal),
        ('GGGGGGGGACCCCC', haltVal),
        ('GAGA', loopVal),
        ('CCCATTTGAGAGGGGG', loopVal),
    ]
    for (inString, solution) in testvals:
        val = utils.runWithTimeout(None, loopIfContainsGAGA, inString)
        utils.tprint(inString, val)
        if val == None:
            assert solution == loopVal
        else:
            assert val == solution
