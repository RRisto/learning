import utils; from utils import rf
import re
from turingMachine import TuringMachine, Transition
from ndTuringMachine import NDTuringMachine
from dfa import Dfa

class Nfa(NDTuringMachine):
    """Represents an nfa as described in the textbook.

    """
    
    epsilonStr = 'Eps'
    """Represents epsilon-transitions in ASCII machine descriptions
    """
    
    def __init__(self, description = None, tapeStr = '', name = None):
        """Initialize Nfa object.

        See NDTuringMachine.__init__() for details.
        """
        NDTuringMachine.__init__(self, description, tapeStr, name)
        self.transformEpsilonTransitions()

    def createRootClone(self, description, tapeStr, name, keepHistory):
        """Create the root clone of this nondeterministic Turing
        machine.
        
        Overrides NDTuringMachine.createRootClone(). See that method
        for documentation.

        """
        return Dfa(description, tapeStr, 0, name, keepHistory=keepHistory)

    def transformAnEpsilonTransition(self, t):
        """Transform an epsilon transition into equivalent transitions without
        epsilon.
        
        Args:

            t (Transition): the epsilon-transition to be transformed

        Returns:

            list of Transition objects: The returned list will contain
                exactly one or two transitions that are not
                epsilon-transitions. Replacing the input transition t
                with these transitions yields an equivalent nfa.

        """
        assert Nfa.epsilonStr in t.label
        assert t.writeSymbol == None
        assert t.direction == TuringMachine.rightDir
        
        # ts will be the list of one or two transitions to be returned.
        ts = []

        # Append a transition that corresponds only to the epsilon,
        # ignoring any other symbols that may be in the label of t.
        # Note that this transition is valid for any scanned symbol
        # (hence the TuringMachine.anySym), and does not consume a tape symbol (hence
        # the TuringMachine.stayDir).
        ts.append(Transition(t.sourceState, t.destState, TuringMachine.anySym, \
                             None, TuringMachine.stayDir))

        # Now we delete the epsilon from the label of t.  If there is
        # anything left, append a standard transition using the
        # remaining label. This standard transition does consume a
        # tape symbol (hence the TuringMachine.rightDir).
        newLabel = t.label.replace(Nfa.epsilonStr, '')
        if newLabel != '':
            ts.append( Transition(t.sourceState, t.destState, newLabel, None, \
                                  TuringMachine.rightDir))

        return ts
        
    def transformEpsilonTransitions(self):
        """Convert into an equivalent nfa with no epsilon-transitions.
        
        """
        newTransitions = dict()
        for sourceState, transitionList in self.rootClone.transitions.items():
            newTransitionList = []
            for t in transitionList:
                if Nfa.epsilonStr in t.label:
                    for newT in self.transformAnEpsilonTransition(t):
                        newTransitionList.append(newT)
                else:
                    newTransitionList.append(t)
            newTransitions[sourceState] = newTransitionList
        self.rootClone.transitions = newTransitions
                    

# see testCheckNfa() in checkTuringMachine.py for more detailed tests
def testNfa():
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
        nfa = Nfa(rf(filename), inString)
        val = nfa.run()
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        assert val == solution
        

