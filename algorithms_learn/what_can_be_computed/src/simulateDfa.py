# SISO program simulateDfa.py

# Simulate a given dfa with a given input. 

# dfaString: ASCII description of the dfa M to be simulated

# inString: the initial content I of M's tape

# returns: 'yes' if M accepts I and 'no' otherwise

# Example:
# >>> simulateDfa(rf('multipleOf5.dfa'), '3425735')
# 'yes'
import utils; from utils import rf; from turingMachine import TuringMachine
import re, sys; from dfa import Dfa
def simulateDfa(dfaString, inString):
    tm = Dfa(dfaString)
    tm.reset(inString)
    tmResult = tm.run()
    return tmResult


# see testCheckDfa() in checkTuringMachine.py for more detailed tests
def testSimulateDfa():
    for (filename, inString, val) in [
            ('containsGAGA.dfa', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.dfa', 'CCCGAGACCAAAAAA', 'yes'),
            ('multipleOf5.dfa', '12345', 'yes'),
            ('multipleOf5.dfa', '1234560', 'yes'),
            ('multipleOf5.dfa', '123456', 'no'),
            ]:
        result = simulateDfa(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result


