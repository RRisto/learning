import utils; from utils import rf
import re
from turingMachine import TuringMachine, Transition

class TwoTDCM(TuringMachine):
    """A TwoTDCM object models a 2TDCM as described in the textbook.

    It does not support blocks or nondeterminism.
    """

    outSymbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    """Symbols that can be written on the output tape -- what Turing would
    call "of the first kind"

    """
    
    maxSteps = 200
    """Best to allow few steps as 2TDCM's often run forever."""

    def writeSymbol(self, symbol):
        """Overrides TuringMachine.writeSymbol().

        Write the given symbol. If it's an output symbol, append to
        the output tape. Otherwise write to the cuurent cell of the
        regular tape.

        """
        if symbol in TwoTDCM.outSymbols:
            self.outTape.append(symbol)
        else:
            TuringMachine.writeSymbol(self, symbol)

    def getOutput(self):
        """Return contents of output tape as a string."""
        return ''.join(self.outTape)

    def getMaxSteps(self):
        """Overrides TuringMachine.getMaxSteps()"""
        return TwoTDCM.maxSteps

    def reset(self, tapeStr = '', state = None, headPos = 0, steps = 0, \
              resetHistory = True):
        """Overrides TuringMachine.reset()"""
        self.outTape = [ ]
        state = TuringMachine.startState if state is None else state
        TuringMachine.reset(self, tapeStr, state, headPos, steps, resetHistory)


def testTwoTDCM():
    for (filename, inString, tapeSoln, outputSoln) in [
            ('containsGAGA.tm', 'CCCCCCCCCAAAAAA', 'no', ''),
            ('containsGAGA.tm', 'CCCGAGACCAAAAAA', 'yes', ''),
            ('loop.tm', 'x', TuringMachine.exceededMaxStepsMsg, ''),
            ('alternating01.tm', '', TuringMachine.exceededMaxStepsMsg, '010101010101010101010101'),
            ('unarySequence.tm', '', TuringMachine.exceededMaxStepsMsg, '0010110111011110111110111111011111110111111110'),
            ]:
        tm = TwoTDCM(rf(filename), inString)
        try:
            tape = tm.run()
        except utils.WcbcException as e:
            if str(e).startswith(TuringMachine.exceededMaxStepsMsg):
                tape = TuringMachine.exceededMaxStepsMsg
            else:
                raise            

        output = tm.getOutput()
        
        utils.tprint('filename:', filename, 'inString:', inString, 'tape:', tape, 'output:', output)
        assert tape == tapeSoln
        if outputSoln == '':
            assert output == outputSoln
        else:
            assert output.startswith(outputSoln)

