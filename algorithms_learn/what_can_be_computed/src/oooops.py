# SISO program oooops.py

# This program is employed in one of the exercises of Chapter 2.
import utils; from utils import rf
def oooops(inString):  
    try:
        val = int(inString)
    except ValueError:
        val = len(inString)
    s = 'A'
    i = 0
    while i != val:
        s += inString[2]
        i += 1
    return s           

# This test will enter an infinite loop.
import sys
def testOooops():
    for inString in ['abc', 'abcdefghij', '008', '5', '-353']:
        print('Trying oooops on "{0}":'.format(inString))
        try:    
            result = oooops(inString)
            utils.tprint(result)
        except:
            utils.tprint("Error:", sys.exc_info()[0])       

