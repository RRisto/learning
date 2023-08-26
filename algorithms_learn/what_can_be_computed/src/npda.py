import utils; from utils import rf
import re
from turingMachine import TuringMachine, Transition
from ndTuringMachine import NDTuringMachine
from nfa import Nfa
from dpda import Dpda

class Npda(NDTuringMachine):
    """Represents an npda as described in the textbook.

    """

    def __init__(self, description = None, tapeStr = '', name = None, \
                 keepHistory = False):
        """Initialize Npda object.

        See NDTuringMachine.__init__() for details.
        """
        NDTuringMachine.__init__(self, description, tapeStr, name, \
                                 keepHistory)

    def createRootClone(self, description, tapeStr, name, keepHistory):
        """Create the root clone of this nondeterministic pda.
        
        Overrides NDTuringMachine.createRootClone(). See that method
        for documentation.

        """
        return Dpda(description, tapeStr, 0, name, keepHistory)

# see testCheckNpda() in checkTuringMachine.py for more detailed tests
def testNpda():
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
        npda = Npda(rf(filename), inString)
        result = npda.run()
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result
    

# This test shows how to examine the history of a computation        
def anotherTestNpda():
    # filename = 'containsGAGA.pda'
    # tape = 'AAAAGGGGAGATT'
    # filename = 'GnTn.pda'
    # tape = 'GGGTTTT'
    # filename = 'GsTs.pda'
    # tape = 'GTTG'
    filename = 'cattag.pda'
    tape = 'CAT'
    npda = Npda(rf(filename), keepHistory=True)
    # npda.printTransitions()
    print('before reset:\n', npda)
    npda.reset(tape)
    print('after reset, before run:\n', npda)
    try:
        result = npda.run()
    except utils.WcbcException as e:
        if str(e).startswith(NDTuringMachine.exceededMaxClonesMsg):
            result = NDTuringMachine.exceededMaxClonesMsg
        else:
            raise            
    print('after run:\n', npda)
    print('result:\n', result)
    print('history:\n' + '\n'.join(npda.acceptingClone.history))

