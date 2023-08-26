import utils; from utils import rf
import re
from turingMachine import TuringMachine, Transition
from nfa import Nfa
from utils import WcbcException

class PdaTransition(Transition):
    """Models a transition in a pda.

    See the documentation of the Transition class for more
    details. PdaTransition objects extend Transition objects because
    they also have information about the stack.

    """
    def __init__(self, sourceState, destState, label, stackLabel, 
                 stackWriteStr, direction):
        """Initialize PdaTransition object.

        Args:

            sourceState (str): the state from which this transition begins, e.g. 'q2'

            destState (str): the state in which this transition ends, e.g. 'q5'

            label (str): the scanned symbol for which this transition
                is followed, e.g. 'G'

            stackLabel (str): the symbol e.g. 'x' that must be on the
            top of the stack for this transition to be followed --
            this symbol is popped when we follow the transition.

            stackWriteStr (str): the symbols e.g. 'xyz' that will be
            pushed onto the stack after this transition is followed.

            direction (str): the direction in which the head moves
                after following this transition. It will be one of
                TuringMachine.rightDir, TuringMachine.leftDir,
                TuringMachine.stayDir.

        """
        Transition.__init__(self, sourceState, destState, label, None, direction)
        self.stackLabel = stackLabel
        self.stackWriteStr = stackWriteStr

    def __str__(self):
        return 'sourceState: %s destState: %s label: %s stackLabel: %s ' \
               'stackWriteStr: %s direction: %s' % \
            (self.sourceState, self.destState, self.label, self.stackLabel, 
             self.stackWriteStr,  self.direction)



class Dpda(TuringMachine):
    """A Dpda object models a dpda as described in the textbook.

    """
    def __init__(self, description = None, tapeStr = '', depth = 0, name = None, \
                 keepHistory = False):
        """Initialize Dpda object.

        Args:

            description (str): A string describing the states and
                transitions of the dpda, according to the
                specification described in the textbook. For an
                example, see the files containsGAGA.pda.

            tapeStr (str): The initial content of the dpda's
                tape.

            depth (int): This dpda could be a "root" machine
                (i.e., it's not being used as a building block in some
                parent machine), in which case its depth is
                zero. Otherwise we store the the depth of this
                building block relative to the root building block.

            name (str): A string that gives a meaningful name to the
                machine, e.g. 'binary incrementer'. This can be used
                for debugging and meaningful output.

            keepHistory (bool): If True, keep a complete record of the
                history of this machine's computation. This is useful
                for certain experiments, but costly in terms of
                storage.

        """
        TuringMachine.__init__(self, description, tapeStr, depth, name, \
                               keepHistory=keepHistory)

    def reset(self, tapeStr = '', state = TuringMachine.startState, headPos = 0, \
              steps = 0, resetHistory=True):
        """Reset the dpda.

        Overrides TuringMachine.reset(). See documentation of that
        method for details.

        """
        self.stack = [] # a list of symbols with the top of the stack last        
        TuringMachine.reset(self, tapeStr, state, headPos, steps, resetHistory)

    def extractTransition(self, line):
        """Given a line in a dpda description, return a new Transition object described by that line.

        Overrides the same method in TuringMachine. We need to
        override because the format is slightly different for dpdas,
        compared to Turing machines.

        Args:

            line (str): a line in a dpda description

        Returns:

            Transition: a new Transition object

        """
        (label, stackWriteStr, sourceState, destState) = \
                self.splitTransition(line)
        if TuringMachine.actionSeparator in stackWriteStr:
            raise WcbcException('transition ' + line + \
                                ' specifies a direction, which is illegal in a pda')
        if TuringMachine.actionSeparator not in label:
            raise WcbcException('transition ' + line + \
                                ' needs both a label and a stack symbol, which can be ' + \
                                Nfa.epsilonStr)
        (label, stackLabel) = [x.strip() for x in \
                                 label.split(TuringMachine.actionSeparator)]
        if label == Nfa.epsilonStr:
            direction = TuringMachine.stayDir
        else:
            direction = TuringMachine.rightDir

        return PdaTransition(sourceState, destState, label, \
                             stackLabel, stackWriteStr, direction)

    def clone(self):
        """Clone this dpda, returning a new Dpda object
        """
        newPda = Dpda(None, self.tape, self.depth, self.name)
        self.copyTMState(newPda)
        newPda.stack = list(self.stack) 
        return newPda


    def isStackEmpty(self):
        """Return True if the stack is empty and False otherwise"""
        return len(self.stack)==0

    def peekStack(self):
        """Return the top element of the stack, or None if the stack is empty."""
        if self.isStackEmpty():
            return None
        else:
            return self.stack[-1]

    def isValidTransition(self, t):
        """Return True if t is a valid transition for the current configuration.
        Args:

            t (Transition): a Transition object

        Returns:

            bool: True if the current scanned symbol matches the label
                of t, and the top of the stack matches the stack
                symbol of t, meaning that t is a transition that can
                be followed from the current configuration.

        """
        scannedSymbol = self.getScannedSymbol()
        stackSymbol = self.peekStack()
        labelEps = (t.label == Nfa.epsilonStr)
        stackReadEps = (t.stackLabel == Nfa.epsilonStr)
        stackEmpty = (stackSymbol is None)

        if not stackReadEps and stackEmpty:
            return False

        # figure out if the label on the transition matches the
        # scanned symbol, storing the result in labelMatches
        if labelEps: # don't need to read anything, so that counts as
                     # a match
            labelMatches = True
        else:
            labelMatches = self.labelMatchesSymbol(scannedSymbol, t.label)

        # figure out if the transition's stack label matches the
        # symbol from the stack, storing the result in stackMatches
        if stackReadEps:
            stackMatches = True
        else:
            stackMatches = self.labelMatchesSymbol(stackSymbol, t.stackLabel)

        return labelMatches and stackMatches

    def applyTransition(self, t):
        """Apply the given transition to the current configuration.

        Overrides TuringMachine.applyTransition(). See that method for
        documentation.

        """
        if t is not None:
            # print('applying transition: ', t)
            if t.stackLabel != Nfa.epsilonStr:
                assert len(self.stack) > 0
                self.stack.pop()
            if t.stackWriteStr != Nfa.epsilonStr:
                # Convention is that the rightmost character of
                # stackWriteStr is pushed first, which is why we now
                # reverse the characters in stackWriteStr
                self.stack.extend([c for c in reversed(t.stackWriteStr)])
        TuringMachine.applyTransition(self, t)
        # print(self)

    def __str__(self):
        return TuringMachine.__str__(self) + ' stack: ' + ''.join(reversed(self.stack))


# see testCheckDpda() in checkTuringMachine.py for more detailed tests
def testDpda():
    for (filename, inString, val) in [
            ('containsGAGA.pda', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.pda', 'CCCGAGACCAAAAAA', 'yes'),
            ('multipleOf5.pda', '12345', 'yes'),
            ('multipleOf5.pda', '1234560', 'yes'),
            ('multipleOf5.pda', '123456', 'no'),
            ]:
        dpda = Dpda(rf(filename), inString)
        result = dpda.run()
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result

# This test shows how to examine the history of a computation        
def anotherTestDpda():
    filename = 'containsGAGA.pda'
    tape = 'GGGGGCCCCGAGATT'
    # filename = 'GnTn.pda'
    # tape = 'GGGTTTT'
    # filename = 'GsTs.pda'
    # tape = 'GTTG'
    dpda = Dpda(rf(filename), keepHistory = True)
    # dpda.printTransitions()
    dpda.reset(tape)
    print('before:\n', dpda)
    result = dpda.run()
    print('after:\n', dpda)
    print('result:\n', result)
    print('history:\n' + '\n'.join(dpda.history))

