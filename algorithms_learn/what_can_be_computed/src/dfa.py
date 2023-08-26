import utils; from utils import rf
import re
from turingMachine import TuringMachine, Transition

class Dfa(TuringMachine):
    """A Dfa object models a dfa as described in the textbook.

    """
    def __init__(self, description = None, tapeStr = '', depth = 0, name = None, \
                 keepHistory = False):
        """Initialize Dfa object.

        Args:

            description (str): A string describing the states and
                transitions of the dfa, according to the
                specification described in the textbook. For examples,
                see the files containsGAGA.dfa and
                multipleOf5.dfa.

            tapeStr (str): The initial content of the dfa's
                tape.

            depth (int): This dfa could be a "root" machine
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

    def extractTransition(self, line):
        """Given a line in a dfa description, return a new Transition object described by that line.

        Overrides the same method in TuringMachine. We need to
        override because the format is slightly different for dfas,
        compared to Turing machines.

        Args:

            line (str): a line in a dfa description

        Returns:

            Transition: a new Transition object

        """
        (states, label) = [x.strip() for x in line.split(TuringMachine.labelSeparator)]
        (sourceState, destState) = [x.strip() for x in states.split(TuringMachine.stateSeparator)]
        return Transition(sourceState, destState, label, None, TuringMachine.rightDir)

    def clone(self):
        """Clone this dfa, returning a new Dfa object
        """
        newDfa = Dfa(None, self.tape, self.depth, self.name)
        self.copyTMState(newDfa)
        return newDfa

    def writeTransition(self, t):
        """Convert a transition into dfa description format.

        Overrides the same method in TuringMachine. We need to
        override because the format is slightly different for dfas,
        compared to Turing machines.

        Args:

            t (Transition): the Transition object to be converted to
                description format

        Returns:

            str: description format of the transition t

        """
        s = TuringMachine.writeTransition(self, t)
        separatorLocation = s.rfind(TuringMachine.writeSymSeparator)
        # epsilon transitions must be treated separately
        if t.label==TuringMachine.anySym and t.direction==TuringMachine.stayDir:
            # it's an epsilon transition -- return whole string
            return s
        else:
            # dfa writes only the label
            return s[:separatorLocation]

    def sortLabelChars(self, s):
        """Sort the characters in the transition label.

        Overrides TuringMachine.sortLabelChars(). See that method for
        additional documentation.

        """
        (prefix, label) = s.split(TuringMachine.labelSeparator, 1)
        sortedLabel = ''.join(sorted(label))
        return prefix + TuringMachine.labelSeparator + sortedLabel
    
# see testCheckDfa() in checkTuringMachine.py for more detailed tests
def testDfa():
    for (filename, inString, val) in [
            ('containsGAGA.dfa', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.dfa', 'CCCGAGACCAAAAAA', 'yes'),
            ('multipleOf5.dfa', '12345', 'yes'),
            ('multipleOf5.dfa', '1234560', 'yes'),
            ('multipleOf5.dfa', '123456', 'no'),
            ]:
        dfa = Dfa(rf(filename), inString)
        result = dfa.run()
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        assert val == result

def testWrite():
    testvals = ['containsGAGA.dfa', 'example2.dfa', 'mult2or3Gs.dfa']
    for filename in testvals:
        s0 = rf(filename)
        tm1 = Dfa(s0)
        s1 = tm1.write()
        tm2 = Dfa(s1)
        s2 = tm2.write()
        utils.tprint(filename, '\n', s0, '\n\n', s1, '\n\n', s2)
        assert tm1.descriptionsAreSame(s0, tm2, s1)
        assert TuringMachine.haveSameTransitions(tm1, tm2)
        assert tm2.descriptionsAreSame(s1, Dfa(s2), s2)
        assert s1 == s2

        
