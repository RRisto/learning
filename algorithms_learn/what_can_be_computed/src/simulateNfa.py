# SISO program simulateNfa.py

# Simulate a given nfa with a given input. 

# nfaString: ASCII description of the nfa M to be simulated

# inString: the initial content I of M's tape

# returns: 'yes' if M accepts I and 'no' otherwise

# Example:
# >>> simulateNfa(rf('simple3.nfa'), 'AGA')
# 'yes'
import utils; from utils import rf; from turingMachine import TuringMachine
import re, sys; from dfa import Dfa; from nfa import Nfa
def simulateNfa(nfaString, inString):
    tm = Nfa(nfaString)
    tm.reset(inString)
    tmResult = tm.run()
    return tmResult



# see testCheckNfa() in checkTuringMachine.py for more detailed tests
def testSimulateNfa():
    for (filename, inString, solution) in [
            ('simple3.nfa', 'AA', 'yes'),
            ('simple3.nfa', 'AGA', 'yes'),
            ('simple3.nfa', 'AC', 'yes'),
            ('simple3.nfa', 'AG', 'yes'),
            ('simple3.nfa', 'ACCGCG', 'yes'),
            ('simple3.nfa', '', 'no'),
            ('simple3.nfa', 'A', 'no'),
            ('simple3.nfa', 'G', 'no'),
            ('simple3.nfa', 'AAA', 'no'),
            ]:
        val = simulateNfa(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        assert val == solution


