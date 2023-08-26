# SISO program simulateDpda.py

# Simulate a given dpda with a given input. 

# pdaString: ASCII description of the dpda M to be simulated

# inString: the initial content I of M's tape

# returns: 'yes' if M accepts I and 'no' otherwise

# Example:
# >>> simulateDpda(rf('multipleOf5.pda'), '3425735')
# 'yes'
import utils; from utils import rf; 
from dpda import Dpda
def simulateDpda(pdaString, inString):
    tm = Dpda(pdaString)
    tm.reset(inString)
    tmResult = tm.run()
    return tmResult
                    

# see testCheckDpda() in checkTuringMachine.py for more detailed tests
def testSimulateDpda():
    for (filename, inString, val) in [
            ('containsGAGA.pda', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.pda', 'CCCGAGACCAAAAAA', 'yes'),
            ('multipleOf5.pda', '12345', 'yes'),
            ('multipleOf5.pda', '1234560', 'yes'),
            ('multipleOf5.pda', '123456', 'no'),
            ]:
        result = simulateDpda(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result


