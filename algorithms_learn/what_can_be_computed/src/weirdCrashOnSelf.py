# SISO program weirdCrashOnSelf.py

# This program is deliberately crafted to enable a certain proof by
# contradiction. Given input string progString representing a python
# program P, weirdCrashOnSelf returns successfully if P(P) causes a
# crash; otherwise, weirdCrashOnSelf crashes.
import utils; from utils import rf
from crashOnSelf import crashOnSelf 
def weirdCrashOnSelf(progString):   
    val = crashOnSelf(progString) 
    if (val == 'yes'):
        return 'did not crash!' 
    else:
        # deliberately crash (divide by zero)
        x = 1 / 0 



def testweirdCrashOnSelf():
    # There is nothing meaningful to assert in this test, because
    # crashOnSelf uses crashOnString, which is an oracle function that
    # does nothing in our implementation.
    try:
        weirdCrashOnSelf('asdf')
    except ZeroDivisionError:
        pass
        
