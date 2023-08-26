# SISO program universal.py

# This is a universal python program -- that is, a python program that
# executes other python programs. Given a program P and input I,
# universal.py returns P(I), provided that P(I) is defined.

# progString: a SISO python program P stored as an ASCII string. See
# the textbook for a formal definition of SISO python program.

# inString: an ASCII string I to be used as input to P.

# returns: If the string P(I) is defined, it is returned. (Recall that
# P(I) is the output of program P on input I.)

# Example:
# >>> universal(rf('containsGAGA.py'), 'CCGAGA')
# 'yes'
import utils; from utils import rf
def universal(progString, inString):  
    # Execute the definition of the function in progString. This defines
    # the function, but doesn't invoke it.
    exec(progString) 
    # Now that the function is defined, we can extract a reference to it.
    progFunction = utils.extractMainFunction(progString, 
                                             locals()) 
    # Invoke the desired function with the desired input string.
    return progFunction(inString) 

def universal1arg(inString):
    progString, newInString = utils.DESS(inString)
    return universal(progString, newInString)

def testUniversal():
    testVals = [
        ('containsGAGA.py', 'asdf', 'no'),
        ('containsGAGA.py', 'GGGGGACCCCGAGATTT', 'yes'),
        ('multiply.py', '100 10000', str(100*10000)),
        ('multiply.py', '1024 256', str(1024*256)),
        ('listEvens.py', '2', ''),
        ('listEvens.py', '10', '2,4,6,8'),
        ]
    for (filename, inString, solution) in testVals:
        val = universal(rf(filename), inString)
        utils.tprint(filename, inString, val)
        assert val == solution
        
def testUniversal1arg():
    testVals = [
        ('containsGAGA.py', 'asdf', 'no'),
        ('containsGAGA.py', 'GGGGGACCCCGAGATTT', 'yes'),
        ('multiply.py', '100 10000', str(100*10000)),
        ('multiply.py', '1024 256', str(1024*256)),
        ('listEvens.py', '2', ''),
        ('listEvens.py', '10', '2,4,6,8'),
        ]
    for (filename, inString, solution) in testVals:
        progString = rf(filename)
        newInString = utils.ESS(progString, inString)
        val = universal1arg(newInString)
        utils.tprint(filename, inString, val)
        assert val == solution
        

