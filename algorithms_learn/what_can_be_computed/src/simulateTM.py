# SISO program simulateTM.py

# Simulate a given Turing machine with a given input. 

# tmString: ASCII description of the machine M to be simulated

# inString: the initial content I of M's tape

# returns: the tape content when M enters a halting state

# Example:
# >>> simulateTM(rf('binaryIncrementer.tm'), 'x100111x')
# 'x101000x'
import utils; from utils import rf;
from turingMachine import TuringMachine
def simulateTM(tmString, inString): 
    # simulate Turing machine described by tmString, with input inString
    # ... 
    tm = TuringMachine(tmString)
    tm.reset(inString)
    tmResult = tm.run()
    return tmResult
                    

# see testCheckTM() in checkTuringMachine.py for more detailed tests
def testSimulateTM():
    for (filename, inString, solution) in [
            ('containsGAGA.tm', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.tm', 'CCCGAGACCAAAAAA', 'yes'),
            ('binaryIncrementer.tm', 'x100111x', 'x101000x'),
            ]:
        val = simulateTM(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        assert val == solution


