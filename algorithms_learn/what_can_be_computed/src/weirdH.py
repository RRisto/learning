# SISO program weirdH.py

# This program is deliberately crafted to enable a certain proof by
# contradiction. It first imports a function H, which is assumed to
# solve HaltsInExpTime in polynomial time. Given input string
# progString representing a python program P, weirdH enters an
# infinite loop if H(P,P) is 'yes'; otherwise, it returns successfully
# (and it can be shown it returns in polynomial time for sufficiently
# long inputs). See chapter 11 for details.

import utils; from utils import rf
# Import H, which is assumed to solve HaltsInExpTime in polynomial 
# time. (In reality, we will prove that H cannot exist.)
from H import H  
def weirdH(progString): 
    if H(progString, progString) == 'yes': 
        # deliberately enter infinite loop
        print('Entering infinite loop...')
        utils.loop() 
    else: 
        # The return value is irrelevant, but the fact that we return
        # right away is important.
        return 'finished already!' 

def testWeirdH():
    msg = 'finished already!'
    testvals = [
        ('factor.py', msg),
        ('multiply.py', msg),
        ('containsGAGA.py', None),
    ]
    for (filename, solution) in testvals:
        val = utils.runWithTimeout(None, weirdH, rf(filename))
        utils.tprint(filename, ':', val)
        assert val == solution
    
