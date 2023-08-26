import utils; from utils import rf
import re
from turingMachine import TuringMachine

class NDTuringMachine:
    """An NDTuringMachine object models a nondeterministic Turing machine
    as described in the textbook.

    """
    
    maxClones = 1000;
    """The maximum number of clones permitted in a single NDTuringMachine object.

    We impose this limit to prevent too many resources being
    consumed. A true, abstract nondeterministic Turing machine should
    of course be permitted as many clones as desired.
    """
    
    exceededMaxClonesMsg = 'Exceeded maximum permitted clones'
    """Message passed to the exception when maximum number of clones is exceeded."""
    
    maxSteps = 100000;
    """The maximum number of computational steps permitted in a computation.

    We impose this limit to prevent too many resources being
    consumed. A true, abstract nondeterministic Turing machine should
    of course be permitted as many steps as desired.
    """

    verbose = False
    """bool: Set this to True to see extensive debugging information at
    each step in the computation.

    """

    def __init__(self, description = None, tapeStr = '', name = None, \
                 keepHistory = False):
        """Initialize NDTuringMachine object.

        Args:

            description (str): A string describing the states and
                transitions of the nondeterministic Turing machine,
                according to the specification described in the
                textbook. For examples, see the files containsGAGA.tm
                and binaryIncrementer.tm.

            tapeStr (str): The initial content of the Turing machine's
                tape.

            name (str): A string that gives a meaningful name to the
                machine, e.g. 'binary incrementer'. This can be used
                for debugging and meaningful output.

            keepHistory (bool): If True, keep a complete record of the
                history of this machine's computation. This is useful
                for certain experiments, but costly in terms of
                storage.

        """

        self.rootClone = self.createRootClone(description, tapeStr, 'root', \
                                              keepHistory)
        """TuringMachine object: The root clone of this nondeterministic
        Turing machine, which is itself a (deterministic) Turing
        machine.

        """
        
        if len(self.rootClone.blocks) > 0:
            msg = "Sorry, blocks aren't supported for nondeterministic machines"
            raise utils.WcbcException(msg)

        self.clones = set([self.rootClone])
        """set of TuringMachine objects: the set of clones that comprise this
        nondeterministic Turing machine.

        """
        
        self.steps = 0
        """int: The number of computational steps taken so far in the computation."""
        
        self.nextCloneID = 1
        """int: Each clone is assigned an ID number sequentially, beginning
        with zero for the root clone. This stores the ID that will be
        assigned to the next clone created.

        """
        
        self.name = name
        self.keepHistory = keepHistory

        self.acceptingClone = None
        """TuringMachine object: mostly for debugging, remember which clone
        accepted (if any)

        """

    def createRootClone(self, description, tapeStr, name, keepHistory):
        """Create the root clone of this nondeterministic Turing machine.

        This is factored out as a method primarily so that derived
        classes can override it. The parameters are as described in
        __init__().

        """
        return TuringMachine(description, tapeStr, 0, name, keepHistory=keepHistory)
        
    def step(self):
        """Perform one computational step in all clones in this
        nondeterministic Turing machine."""
        
        self.steps += 1
        victims = set()
        children = set()
        for tm in self.clones:
            ts = tm.getValidTransitions()
            if len(ts) == 0:
                victims.add(tm)
            else:
                for i in range(1,len(ts)):
                    child = tm.clone()
                    child.name = 'clone' + str(self.nextCloneID)
                    self.nextCloneID += 1
                    child.applyTransition(ts[i])
                    children.add(child)
                tm.applyTransition(ts[0])
        self.clones -= victims
        self.clones |= children

    def run(self):
        """Run the nondeterministic Turing machine until it halts.

        For practical reasons, the machine will also stop once it
        exceeds its maximum number of steps.

        """
        while True:
            if NDTuringMachine.verbose: print(self); print()
            self.step()
            allReject = True
            retVal = None
            for tm in self.clones:
                if tm.state != TuringMachine.rejectState:
                    allReject = False
                if tm.state == TuringMachine.acceptState:
                    retVal = 'yes'
                elif tm.state == TuringMachine.haltState:
                    retVal = ''.join(tm.tape)
                # Mostly for debugging, remember which clone accepted
                # (if any). Also, we break so that the first clone to
                # accept is the one whose return value is used.
                if tm.state == TuringMachine.acceptState or \
                   tm.state == TuringMachine.haltState:
                    self.acceptingClone = tm
                    break
            if allReject:
                retVal = 'no'
            if retVal != None:
                return retVal
            if self.steps >= NDTuringMachine.maxSteps:
                self.rootClone.raiseExceededMaxSteps()
                # return NDTuringMachine.exceededMaxStepsMsg
            if len(self.clones) > self.maxClones:
                raise utils.WcbcException(NDTuringMachine.exceededMaxClonesMsg)
                # return NDTuringMachine.exceededMaxClonesMsg

    def reset(self, tapeStr = '', state = TuringMachine.startState, headPos = 0, \
              steps = 0, resetHistory=True):
        """Reset the Turing machine.

        See the documentation of TuringMachine.reset() for details.

        """
        
        self.rootClone.reset(tapeStr, state, headPos, steps, resetHistory)
        self.clones = set([self.rootClone])
        self.steps = steps

    def printTransitions(self):
        """Print the transitions of this machine"""
        self.rootClone.printTransitions()

    # get a list of the possible transitions from the given state
    def getTransitions(self, state):
        """Return a list of the possible transitions from the given state.

        See TuringMachine.getTransitions() for details.
        """
        return self.rootClone.getTransitions(state)

    def __str__(self):
        maxClonesToPrint = 10
        tm_strings = [str(tm) for tm in list(self.clones)[:maxClonesToPrint]]
        if len(self.clones) > maxClonesToPrint:
            tm_strings.append('... [and other clones]')
        return 'steps: ' + str(self.steps) + ' num clones: ' + str(len(self.clones)) + \
            '\n' + '\n'.join(tm_strings)

    def __repr__(self):
        return self.__str__()

    def write(self):
        """Convert the current Turing machine into description format.

        See TuringMachine.write() for details.

        """
        return self.rootClone.write()

    def labelMatchesSymbol(self, symbol, label):
        return self.rootClone.labelMatchesSymbol(symbol, label)

# see testCheckNDTM() in checkTuringMachine.py for additional tests
def testNDTuringMachine():
    for (filename, inString, solution) in [
            ('containsGAGAorGTGT.tm', 'GTGAGAGAGT', 'yes'),
            ('containsGAGAorGTGT.tm', 'GTGAGTGTGT', 'yes'),
            ('containsGAGAorGTGT.tm', 'GTGAGTGAGT', 'no'),
            ('manyClones.tm', 'CGCGCGCGCGCGCGCCCCCCCCC', NDTuringMachine.exceededMaxClonesMsg),
            ('loop.tm', 'x', TuringMachine.exceededMaxStepsMsg),
            ('GthenOneT.tm', 'xCCCCCTCCGTTx', 'yes'),
            ('GthenOneT.tm', 'xCCCCCCCGTTGCATGx', 'yes'),
            ('GthenOneT.tm', 'xCCTCCTCCGTTx', 'no'),
            ('GthenOneT.tm', 'xCCCCCCCGTTGCATGTTx', 'no'),
            ('GthenOneT.tm', 'xGTx', 'yes'),
            ]:
        ndtm = NDTuringMachine(rf(filename), inString, keepHistory=True)
        try:
            result = ndtm.run()
        except utils.WcbcException as e:
            if str(e).startswith(NDTuringMachine.exceededMaxClonesMsg):
                result = NDTuringMachine.exceededMaxClonesMsg
            elif str(e).startswith(TuringMachine.exceededMaxStepsMsg):
                result = TuringMachine.exceededMaxStepsMsg
            else:
                raise            
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', result)
        if result=='yes':
            utils.tprint('acceptingClone:', ndtm.acceptingClone)
            utils.tprint('history:\n' + '\n'.join(ndtm.acceptingClone.history))
        assert result == solution
