# Python file showCATTAGhist.py

# This file can be used to print details of a computation by the npda
# 'cattag.pda' described in the appendix.

# Example:
# >>> showCATTAGhist(True) 

import utils; from utils import rf
from npda import Npda

def showCATTAGhist(printResults = True):
    """Print details of the computation of 'cattag.pda' on input 'CAT'

    Args:
    
        printResults (bool): If True, details will be
            printed. Otherwise, nothing will be printed. The end-user
            almost certainly will want printResults = True, but it is
            useful for test code to be able to suppress the output.

    Returns:

       str: The output of the competition is returned, which in this
            case should be 'yes'.

    """
    npda = Npda(rf('cattag.pda'), 'CAT', keepHistory=True)
    result = npda.run()
    if printResults:
        print('result: ', result)
        print('\nconfiguration after halting:\n', npda)
        print('\nhistory of accepting clone:\n' + '\n'.join(npda.acceptingClone.history))
    return result

def testShowCATTAGhist(printResults = False):
    val = showCATTAGhist(printResults)
    assert val == 'yes'
    
