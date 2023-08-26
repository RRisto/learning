# SISO program simulateTM1.py

# Simulate a given Turing machine with a given input. Identical to
# simulateTM.py except that simulateTM1.py receives only one string
# parameter.

# inString: encodes two strings M, I (via utils.ESS), where M is the
# ASCII description of the machine M to be simulated and I is the
# initial content I of M's tape.

# returns: the tape content when M enters a halting state

# Example:
# >>> simulateTM1(utils.ESS(rf('binaryIncrementer.tm'), 'x100111x'))
# 'x101000x'
import utils; from utils import rf
from simulateTM import simulateTM 
def simulateTM1(inString):
    (progString, newInString) = utils.DESS(inString)
    return simulateTM(progString, newInString) 


def testSimulateTM1():
    for (filename, inString, solution) in [
            ('containsGAGA.tm', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.tm', 'CCCGAGACCAAAAAA', 'yes'),
            ('binaryIncrementer.tm', 'x100111x', 'x101000x'),
            ]:
        val = simulateTM1(utils.ESS(rf(filename), inString))
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        assert val == solution


