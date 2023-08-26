# SISO program simulateNpda.py

# Simulate a given npda with a given input. 

# npdaString: ASCII description of the npda M to be simulated

# inString: the initial content I of M's tape

# returns: 'yes' if M accepts I and 'no' otherwise

# Example:
# >>> simulateNpda(rf('multipleOf5.pda'), '3425735')
# 'yes'
import utils; from utils import rf; 
from npda import Npda
def simulateNpda(pdaString, inString):
    tm = Npda(pdaString)
    tm.reset(inString)
    tmResult = tm.run()
    return tmResult
                    
# see testCheckNpda() in checkTuringMachine.py for more detailed tests
def testSimulateNpda():
    for (filename, inString, val) in [
            ('containsGAGA.pda', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.pda', 'CCCGAGACCAAAAAA', 'yes'),
            ('multipleOf5.pda', '12345', 'yes'),
            ('multipleOf5.pda', '1234560', 'yes'),
            ('multipleOf5.pda', '123456', 'no'),
            ('evenPalindromes.pda', '', 'yes'),
            ('evenPalindromes.pda', 'AA', 'yes'),
            ('evenPalindromes.pda', 'TT', 'yes'),
            ('evenPalindromes.pda', 'ATTA', 'yes'),
            ('evenPalindromes.pda', 'AATTTTAA', 'yes'),
            ('evenPalindromes.pda', 'A', 'no'),
            ('evenPalindromes.pda', 'T', 'no'),
            ('evenPalindromes.pda', 'AATT', 'no'),
            ('evenPalindromes.pda', 'ATA', 'no'),
            ]:
        result = simulateNpda(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result

