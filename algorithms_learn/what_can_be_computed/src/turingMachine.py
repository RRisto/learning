import utils; from utils import rf
import re

class Transition:
    """Models a transition in a Turing machine.

    Example: Consider a transition from state q2 to q5, which is
    followed if the scanned symbol is 'G', rewriting the symbol as a
    'T' then moving the head to the right. In the terminology of this
    class, q2 is the sourceState, q5 is the destState, G is the label,
    T is the writeSymbol, and right is the direction.

    """
    
    def __init__(self, sourceState, destState, label, writeSymbol, direction):
        """Initialize Transition object.

        Args:

            sourceState (str): the state from which this transition begins, e.g. 'q2'

            destState (str): the state in which this transition ends, e.g. 'q5'

            label (str): the scanned symbol for which this transition
                is followed, e.g. 'G'

            writeSymbol (str): the symbol that will overwrite the
                scanned symbol, or None to leave the scanned symbol
                unchanged

            direction (str): the direction in which the head moves
                after following this transition. It will be one of
                TuringMachine.rightDir, TuringMachine.leftDir,
                TuringMachine.stayDir.

        """
        self.sourceState = sourceState
        self.destState = destState
        self.label = label
        self.writeSymbol = writeSymbol
        self.direction = direction

    def __str__(self):
        return 'sourceState: %s destState: %s label: %s writeSymbol: %s direction: %s' % \
            (self.sourceState, self.destState, self.label, self.writeSymbol, self.direction)

    def __repr__(self):
        return self.__str__()
    
    # Static method to unify the labels of compatible transitions
    @staticmethod
    def unify(tList):
        """Unify the transitions in a list of compatible transitions.

        Transitions are compatible if they have the same source state,
        destination state, write symbol, and direction. That is, they
        may differ in their label but nothing else. Sometimes it is
        convenient to unify compatible transitions by transforming
        them into a single transition with a new label that
        incorporates all of the input transitions. This method returns
        a single transition that unifies a given list of transitions,
        which must themselves all be compatible.

        Args:

            tList (list of Transition objects): the list of compatible
                transitions that will be unified.

        Returns:

            Transition: a single unified transition representing all
                transitions in tList.

        """
        assert len(tList)>0
        first = tList[0]
        unifiedTrans = Transition(first.sourceState, first.destState, None, first.writeSymbol, first.direction)
        for t in tList:
            assert unifiedTrans.isCompatible(t)
        labels = [t.label for t in tList]
        unifiedTrans.label = ''.join(labels)
        return unifiedTrans

    def isCompatible(self, other):
        """Determine whether this transition is compatible with the other transition.

        Transitions are compatible if they have the same source state,
        destination state, write symbol, and direction. That is, they
        may differ in their label but nothing else. This method
        returns True if this transition is compatible with the other
        transition, and False otherwise.

        Args:

            other (Transition): A Transition object to be compared
                with the calling Transition object.

        Returns:

            bool: True if this transition is compatible with the other
                transition, and False otherwise

        """
        
        return self.sourceState == other.sourceState \
            and self.destState == other.destState \
            and self.writeSymbol == other.writeSymbol \
            and self.direction == other.direction

    def __eq__(self, other):
        if self is other: return True
        if other==None: return False
        if not isinstance(other, Transition): return False
        return self.sourceState == other.sourceState \
                and self.destState == other.destState \
                and self.label == other.label \
                and self.writeSymbol == other.writeSymbol \
                and self.direction == other.direction

    def __ne__(self, other):
        return not self==other

    def __lt__ (self, other):
        return (self.sourceState, self.destState, self.label, \
                self.writeSymbol, self.direction) \
            < \
            (other.sourceState, other.destState, other.label, \
             other.writeSymbol, other.direction)

    def __gt__ (self, other):
        return other.__lt__(self)

    def getKeyForUnify(self):
        """Returns a key that can be used for collecting compatible transitions.

        See isCompatible() for a description of transition
        compatibility.

        Returns:

            (src, dest, writeSym, dir): a 4-tuple of str, consisting
                of the four attributes that determine with the
                transitions are compatible with each other.

        """
        return (self.sourceState, self.destState, self.writeSymbol, self.direction)

    @staticmethod
    def reassembleFromUnifyKey(key, label):
        """Re-create a transition from its compatibility key and label.

        See isCompatible() for a description of transition
        compatibility. See getKeyForUnify() for a description of
        compatibility keys. This method takes the 4-tuple
        compatibility key and returns a new Transition object
        compatible with that key and the given label.

        Args:

            key (4-tuple of str: (src, dest, writeSym, dir)): A
            compatibility key.

            label (str): the label for the new transition

        Returns:

            Transition: New transition object with the given label and
                compatibility key.

        """
        return Transition(key[0], key[1], label, key[2], key[3])


class TuringMachine:
    """A TuringMachine object models a Turing machine as described in the
    textbook.

    """
    
    verbose = False
    blockMarker = 'block:'
    maxSteps = 100000
    maxDepth = 1000
    exceededMaxStepsMsg = 'exceeded maxSteps'
    rightDir = 'R'
    leftDir = 'L'
    stayDir = 'S'
    noStr = 'no'
    yesStr = 'yes'
    # An underscore character represents blanks in this model of a
    # Turing machine. Technically, this means the Turing machines
    # models here are not the same as the ones in the textbook,
    # because the textbook Turing machines employ the ASCII alphabet,
    # and the underscore character is an element of that alphabet. We
    # prefer to accept that inconsistency rather than using a more
    # complex method for modeling blanks.
    blank = '_' 

    # As with the blank symbol above, the following characters have
    # special meaning in our Turing machine representation, and are
    # therefore not permitted as part of the alphabet.  Whitespace
    # characters are also excluded from the alphabet.
    anySym = '~' # Stands for any one symbol
    notSym = '!' # Stands for any symbol not in the immediately following sequence
    commentStart = '#'
    actionSeparator = ','
    blockSeparator = '='
    stateSeparator = '->'
    labelSeparator = ':'
    writeSymSeparator = ';'

    validSymbols = {c for c in
        r"""$'"%&()*+-./0123456789<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"""}
    
    acceptState = 'qA'
    rejectState = 'qR'
    haltState = 'qH'
    startState = 'q0'
    
    def __init__(self, description = None, tapeStr = '', depth = 0, name = None, \
                 allowImplicitReject = True, \
                 allowLeftFromCell0 = True, \
                 keepHistory = False):
        """Initialize TuringMachine object.

        Args:

            description (str): A string describing the states and
                transitions of the Turing machine, according to the
                specification described in the textbook. For examples,
                see the files containsGAGA.tm and
                binaryIncrementer.tm.

            tapeStr (str): The initial content of the Turing machine's
                tape.

            depth (int): This Turing machine could be a "root" machine
                (i.e., it's not being used as a building block in some
                parent machine), in which case its depth is
                zero. Otherwise we store the the depth of this
                building block relative to the root building block.

            name (str): A string that gives a meaningful name to the
                machine, e.g. 'binary incrementer'. This can be used
                for debugging and meaningful output.

            allowImplicitReject (bool): If we encounter a state for
                which there is no explicitly listed transition, we can
                implicitly assume this is a transition to the reject
                state. According to the textbook definition,
                allowImplicitReject should be True. But sometimes it
                is convenient to set it to False for debugging
                purposes, since it will prevent us unintentionally
                rejecting certain inputs.

            allowLeftFromCell0 (bool): If we are already at cell 0 and
                we are commanded to move left, ignore the command and
                remain at cell 0. If allowLeftFromCell0 is False,
                throw an exception when commanded to move left from
                cell 0. According to the textbook definition,
                allowLeftFromCell0 should be True. But sometimes it is
                convenient to set it to False for debugging purposes.

            keepHistory (bool): If True, keep a complete record of the
                history of this machine's computation. This is useful
                for certain experiments, but costly in terms of
                storage.
        """

        # 'transitions' is a dictionary whose key is state, and value
        # is list of transitions leaving that state.  Each transition
        # is stored as a Transition object.
        self.transitions = None

        # This Turing machine could be a "root" machine (i.e., it's not
        # being used as a building block in some parent machine), in
        # which case its depth is zero. Otherwise we store the the
        # depth of this building block relative to the root building
        # block.
        self.depth = depth

        # The name of the machine can be used for debugging and meaningful output.
        self.name = name

        # If we encounter a state for which there is no explicitly
        # listed transition, we can implicitly assume this is a
        # transition to the reject state. According to the textbook
        # definition, allowImplicitReject should be True. But
        # sometimes it is convenient to set it to False for debugging
        # purposes, since it will prevent us unintentionally rejecting
        # certain inputs.
        self.allowImplicitReject = allowImplicitReject

        # If we are already at cell 0 and we are commanded to move
        # left, ignore the command and remain at cell 0. If
        # allowLeftFromCell0 is False, throw an exception when
        # commanded to move left from cell 0. According to the
        # textbook definition, allowLeftFromCell0 should be True. But
        # sometimes it is convenient to set it to False for debugging
        # purposes.
        self.allowLeftFromCell0 = allowLeftFromCell0
        
        # Dictionary of building blocks used in this machine. Key is
        # the state from which we jump to the building block, value is
        # the building block itself (i.e., a Python object of type
        # TuringMachine)
        self.blocks = dict()

        # If True, keep a complete record of the history of this
        # machine's computation. This is useful for certain
        # experiments, but costly in terms of storage.
        self.keepHistory = keepHistory

        # list of strings giving config at each step
        self.history = None

        self.reset(tapeStr, resetHistory=True)
        if description:
            self.read(description)
        self.checkAllSymbolsValid()


    def splitTransition(self, line):
        """Given a line in a Turing machine description, split into transition components.

        Args:

            line (str): a line in a Turing machine description

        Returns:

            4-tuple of str (label, actions, sourceState, destState):
                where label, sourceState, destState are attributes as
                described in the documentation for the Transition
                class, and actions is a string containing the write
                symbol, if any, and the direction.

        """
        
        # Define a character set consisting of the label separator and
        # the write symbol separator.
        splitRegex = '[' + \
                     TuringMachine.labelSeparator + \
                     TuringMachine.writeSymSeparator + \
                     ']'
        # Split on the above two separators
        (states, label, actions) = [x.strip() for x in re.split(splitRegex,line)]
        # Split into source and destination state
        (sourceState, destState) = \
            [x.strip() for x in states.split(TuringMachine.stateSeparator)]
        return (label, actions, sourceState, destState)

    def extractTransition(self, line):
        """Given a line in a Turing machine description, return a new Transition object described by that line.

        Args:

            line (str): a line in a Turing machine description

        Returns:

            Transition: a new Transition object

        """
        (label, actions, sourceState, destState) = \
                self.splitTransition(line)
        if TuringMachine.actionSeparator in actions:
            (writeSymbol, direction) = \
                [x.strip() for x in actions.split(TuringMachine.actionSeparator)]
        else:
            (writeSymbol, direction) = (None, actions)
        return Transition(sourceState, destState, label, writeSymbol, direction)

    @staticmethod
    def stripComments(lines):
        """Strip comments from a Turing machine description.

        A comment is anything after a '#' chaacter on a given line.

        Args:

            lines (list of str): list of lines in the Turing machine
                description.

        Returns:

            list of str: The same list of Turing machine description
                lines with comments removed.

        """

        return [x.split(TuringMachine.commentStart)[0] for x in lines]

    
    def read(self, tmString):
        """Build the states and transitions of a Turing machine from an ASCII description.

        This method creates the self.transitions dictionary attribute,
        and populates it with the transitions in the given
        description. Nothing is returned. This method can also deal
        with building blocks, recursively reading descriptions of any
        building blocks encountered and adding them to the current
        machine.

        Args:

            tmString (str): Turing machine description.

        """

        self.transitions = dict()
        # split on newlines
        tmLines = tmString.split('\n')
        # strip comments
        tmLines = TuringMachine.stripComments(tmLines)
        # strip whitespace
        tmLines = [x.strip() for x in tmLines]
        for line in tmLines:
            if len(line)>0:
                if line.startswith(TuringMachine.blockMarker):
                    self.addBlock(line)
                else:
                    t = self.extractTransition(line)
                    self.addTransition(t)

    def writeTransition(self, t):
        """Convert a transition into Turing machine description format.

        Args:

            t (Transition): the Transition object to be converted to
                description format

        Returns:

            str: description format of the transition t

        """

        components = [t.sourceState, TuringMachine.stateSeparator, t.destState,
                      TuringMachine.labelSeparator, ' ', t.label,
                      TuringMachine.writeSymSeparator]
        if t.writeSymbol != None:
            components += [t.writeSymbol, TuringMachine.actionSeparator]
        components.append(t.direction)
        return ''.join(components)
            
    def write(self):
        """Convert the current Turing machine into description format.

        Returns:

            str: description format of the current machine, suitable
                for storing in a .tm file.

        """

        if len(self.blocks)>0:
            raise utils.WcbcException("Error: writing Turing machines is not implemented for blocks.")
        if self.transitions == None: 
            return '[No transitions]'
        lines = []
        for tList in self.transitions.values():
            for t in tList:
                line = self.writeTransition(t)
                lines.append(line)
        lines.sort()
        return '\n'.join(lines)

    def addBlock(self, line):
        """Add a building block to the current machine.

        Args:

            line (str): A line in a Turing machine description that
                requests the insertion of a block. For an example, see
                the file countCs.tm.

        """

        if self.depth == TuringMachine.maxDepth:
            message = 'Exceeded max depth when adding block in line "%s"' % line
            raise utils.WcbcException(message)
        # Remove the initial block marker
        line = line[len(TuringMachine.blockMarker):]
        # Partition on the TuringMachine.blockSeparator
        (state, separator, filename) = \
            [x.strip() for x in line.partition(TuringMachine.blockSeparator)]
        if separator != TuringMachine.blockSeparator:
            message = 'Unexpected separator in block description '
            raise utils.WcbcException(message)
        newBlock = TuringMachine(rf(filename), '', self.depth+1)
        self.blocks[state] = newBlock

    def getScannedSymbol(self):
        """Return the symbol currently scanned by the machine.

        Returns:

            str: The return value will be a single character, which is
                the value of the tape cell at the current position.

        """
        return self.tape[self.headPos]

    def labelMatchesSymbol(self, symbol, label):
        """Return True if the given symbol is valid for a transition with the given label.

        Usually, this will return True if symbol is one of the
        characters in label, but this method also handles certain
        special cases, such as the special symbol that matches any
        character, and the use of '!' for "not".

        Args:

            symbol (str): a single character

            label (str): the label attribute of a Transition. See the
                Transition documentation.

        Returns:

            bool: True if the symbol is valid for a transition
                with the given label, and False otherwise.

        """

        if TuringMachine.anySym == label:
            return True
        elif label[0] == TuringMachine.notSym:
            return symbol not in label[1:]
        elif symbol in label:
            return True
        else:
            return False
        

    # is t a valid transition?
    def isValidTransition(self, t):
        """Return True if t is a valid transition for the current configuration.

        Args:

            t (Transition): a Transition object

        Returns:

            bool: True if the current scanned symbol matches the label
                of t, meaning that t is a transition that can be
                followed from the current configuration.

        """

        scannedSymbol = self.getScannedSymbol()
        return self.labelMatchesSymbol(scannedSymbol, t.label)


    # get a list of the possible transitions from the given state
    def getTransitions(self, state):
        """Return a list of the possible transitions from the given state.

        This ignores the scanned symbol. The returned transitions are
        all the transitions that could ever be followed from the
        given state.

        Args:

            state (str): a state in the Turing machine

        Returns:

            list of Transition objects: A list containing all
                transitions whose source state is the given state
                parameter. This could be the empty list.

        """
        return self.transitions.get(state, [])


    def getValidTransitions(self):
        """Return a list of all valid transitions from the current configuration.

        This is a list of all transitions from the current state whose
        label matches the current scanned symbol.

        Returns:

            list of Transition objects: A list containing all valid
                transitions from the current configuration. This could
                be the empty list.

        """
        transitionList = self.getTransitions(self.state)
        ts = []
        for t in transitionList:
            if self.isValidTransition(t):
                ts.append(t)
        return ts

    def writeSymbol(self, symbol):
        """Write the given symbol onto the tape at the current head position.

        Args:

            symbol (str): a single character to be written onto the tape

        """
        self.tape[self.headPos] = symbol

    @staticmethod
    def isAHaltingState(state):
        """True if the given state is a halting state, and False otherwise."""
        return state == TuringMachine.acceptState or \
            state == TuringMachine.rejectState or \
            state == TuringMachine.haltState

    def applyTransition(self, t):
        """Apply the given transition to the current configuration.

        This implements one computational step of the Turing machine,
        following the given transition to its destination state,
        writing a symbol onto the tape if necessary, and moving the
        head if necessary.

        Args:

            t (Transition): the Transition to be followed. If t is
                None and implicit rejection is permitted, the machine
                will transition into the project state.

        """
        if TuringMachine.verbose: print('Applying transition', t)
        self.steps = self.steps + 1
        if not t:
            if self.allowImplicitReject:
                self.state = TuringMachine.rejectState
            else:
                message = '***Error***: No valid transition was found, and implicit rejects are disabled.\n' + \
                              'Current configuration:\n' + str(self)
                raise utils.WcbcException(message)
        else:
            self.state = t.destState
        if self.isAHaltingState(self.state):
            self.halted = True
        if t:
            if t.writeSymbol:
                self.writeSymbol(t.writeSymbol)
            if t.direction == TuringMachine.leftDir:
                if self.headPos > 0:
                    self.headPos = self.headPos - 1
                elif self.allowLeftFromCell0:
                    pass # we remain in cell 0
                else:
                    message = '***Error***: Tried to move left ' + \
                              'from cell 0, which is disallowed by ' + \
                              'this Turing machine.\n' + \
                              'Current configuration:\n' + str(self)
                    raise utils.WcbcException(message)
            elif t.direction == TuringMachine.rightDir:
                self.headPos = self.headPos + 1
                if self.headPos == len(self.tape):
                    self.tape.append(TuringMachine.blank)
        if self.keepHistory:
            self.history.append(str(self))



    def runBlock(self):
        """Run a building block from the current state."""
        block = self.blocks[self.state]
        block.reset(self.tape, TuringMachine.startState, self.headPos)
        block.run()
        self.steps = self.steps + block.steps
        self.tape = block.tape
        self.headPos = block.headPos
        if block.state == TuringMachine.rejectState:
            self.state = TuringMachine.rejectState
            self.halted = True

    def step(self):
        """Perform one computational step for this Turing machine."""
        ts = self.getValidTransitions()
        if len(ts) > 1:
            message = '***Error***: multiple valid transitions in deterministic Turing machine.\n' + \
                      'Current state:' + self.state + '\n' + \
                      'Valid transitions:' + str(ts)
            raise utils.WcbcException(message)
        if len(ts) == 0:
            t = None
        else:
            t = ts[0]
        self.applyTransition(t)
        if self.state in self.blocks:
            self.runBlock()

    def __str__(self):
        if self.name:
            name = self.name + ': '
        else:
            name = ''
        return name + 'steps: %d tape: "%s" state: %s, headPos: %d' % \
            (self.steps, ''.join(self.tape), self.state, self.headPos)

    def __repr__(self):
        return self.__str__()

    def getOutput(self):
        """Return the output of the Turing machine.

        By definition, the output of a Turing machine is the tape
        contents up to but not including the first blank.

        Returns:

            str: output of the Turing machine

        """
        
        # Find the index of the first blank on the tape.
        if TuringMachine.blank not in self.tape:
            blankIndex = len(self.tape) # there is an implicit a blank
                                        # at the end of the tape
        else:
            blankIndex = self.tape.index(TuringMachine.blank)
        return ''.join(self.tape[:blankIndex])

    def getMaxSteps(self):
        return TuringMachine.maxSteps

    def run(self):
        """Run the Turing machine until it halts.

        For practical reasons, the machine will also stop once it
        exceeds its maximum number of steps.

        """
        while not self.halted and self.steps < self.getMaxSteps():
##            print('before step %d:' % self.steps)
##            print('tape:', self.tape)
##            print('state:', self.state)
##            print('headPos:', self.headPos)
            self.step()
##            print('after that step (now step=%d)' % self.steps)
##            print('tape:', self.tape)
##            print('state:', self.state)
##            print('headPos:', self.headPos)
##            print()
        if self.state == TuringMachine.acceptState:
            return TuringMachine.yesStr
        elif self.state == TuringMachine.rejectState:
            return TuringMachine.noStr
        elif self.state == TuringMachine.haltState:
            return self.getOutput()
        else:
            assert self.steps >= self.getMaxSteps()
            self.raiseExceededMaxSteps()

    def raiseExceededMaxSteps(self):
        """Raise an exception indicating that the maximum number of steps was exceeded.
        """
        
        raise utils.WcbcException(TuringMachine.exceededMaxStepsMsg + \
                                  '.  Current output: ' + self.getOutput())        
        
    def reset(self, tapeStr = '', state = None, headPos = 0, steps = 0, \
              resetHistory = True):
        """Reset the Turing machine.

        This is typically used to run a fresh computation on the
        machine, but optional parameters allow the machine to be set
        up in more specific configurations.

        Args:

            tapeStr (str): The initial content of the Turing machine's
                tape.

            state (str): The state in which the Turing machine should
                begin computing. By default, this will be the Turing
                machine's predefined initial state, but it can be
                something else.

            headPos (int): The initial location of the tape head,
                which defaults to zero.

            steps (int): The number of computational steps this
                machine has already performed. Usually this would be
                zero, but for certain experiments we want to reset the
                machine as if it has already done a certain amount of
                work.

            resetHistory (bool): If True, delete any history of
                previous computations.

        """

        self.tape = [c for c in tapeStr]
        self.state = TuringMachine.startState if state is None else state
        self.headPos = headPos
        self.halted = False
        self.steps = steps
        # append blanks up to the head position if necessary
        if self.headPos >= len(self.tape):
            numBlanksNeeded = self.headPos - len(self.tape) + 1
            for i in range(numBlanksNeeded):
                self.tape.append(TuringMachine.blank)
        if self.keepHistory and resetHistory:
            # list of strings giving config at each step
            self.history = [ str(self) ]

    def copyTMState(self, dest):
        """Copy most of the state of this Turing machine to the destination machine.

        This is a helper to the clone() method, factored out so that
        derived classes can implement their own clone() then call this
        helper. Copies the transitions, blocks and history attributes
        to the destination then resets it.

        Args:

            dest (TuringMachine): Destination machine to which state
                will be copied.

        """
        dest.transitions = self.transitions
        dest.blocks = self.blocks
        dest.keepHistory = self.keepHistory
        if self.keepHistory:
            dest.history = list(self.history)
        dest.reset(self.tape, self.state, \
                    self.headPos, self.steps, resetHistory=False)
                
    def clone(self):
        """Clone this machine, returning a new TuringMachine
        """
        newTM = TuringMachine(None, self.tape, self.depth, self.name)
        self.copyTMState(newTM)
        return newTM

    def printTransitions(self):
        """Print the transitions of this machine"""
        for t in self.transitions.values():
            print(t)

    def addTransition(self, t):
        """Add a transition to this machine.

        Args:

            t (Transition): the Transition object to be added
        """
        if self.transitions == None:
            self.transitions = dict()
        transitionList = self.transitions.setdefault(t.sourceState, [])
        transitionList.append(t)

    def checkSymbolIsValid(self, t, c):
        """Check if a given symbol is permitted in Turing machines.

        Nothing is returned, but a WcbcException is raised if the
        symbol is invalid.

        Args:

            t (Transition): the Transition in which c is used.

            c (str): a single character which is the symbol to be
                checked

        """
        if c not in TuringMachine.validSymbols:
            message = '''***Error***: The symbol {0} (ASCII value {1}) is not permitted in Turing machine alphabets. The full transition containing this error is:\n{2}'''.format(c, ord(c), t)
            raise utils.WcbcException(message)
            

    def checkAllSymbolsValid(self):
        """Check that all symbols used in this machine are permitted.

        Nothing is returned, but a WcbcException is raised if a
        symbol is invalid.
        """
        if self.transitions:
            for tList in self.transitions.values():
                for t in tList:
                    label = t.label
                    if label==TuringMachine.anySym:
                        continue
                    elif label[0]==TuringMachine.notSym:
                        label = label[1:]
                    for c in label:
                        self.checkSymbolIsValid(t, c)

    @staticmethod
    def haveSameTransitions(tm1, tm2):
        """Determine whether two Turing machines have the same transitions.

        Args:

            tm1 (TuringMachine): first Turing machine to be compared

            tm2 (TuringMachine): second Turing machine to be compared

        Returns:

           bool: True if the two given Turing machines have
               transitions that are equivalent, and False otherwise.

        """
        return tm1.hasSameTransitions(tm2) and tm2.hasSameTransitions(tm1)

    def hasSameTransitions(self, other):
        """Determine whether every transition and this Turing machine exists in the other machine.

        This method is not symmetric in the parameters. It checks if
        every transition in self has a corresponding transition in
        other, but other may have additional transitions.

        Args:

            other (TuringMachine): machine whose transitions will be
                compared with the current machine

        Returns:

            bool: True if every transition in self has a corresponding
               transition in other.

        """
        for state, tList in self.transitions.items():
            otherTList = other.getTransitions(state)
            for t in tList:
                otherCompatible = [tr for tr in otherTList if t.isCompatible(tr)]
                for c in TuringMachine.validSymbols:
                    if self.labelMatchesSymbol(c, t.label):
                        foundMatch = False
                        for otherTrans in otherCompatible:
                            if self.labelMatchesSymbol(c, otherTrans.label):
                                foundMatch = True
                                break
                        if not foundMatch:
                            return False
        return True

    def sortLabelChars(self, s):
        """Sort the characters in the transition label.

        We are given a line of a Turing machine description, and an
        equivalent line is returned. The only difference is that if
        there are multiple characters in the transition label, these
        characters are sorted into ascending order. This brings the
        description into a standard form that can be compared against
        other machines more easily.

        Args:

            s (str): a line of a Turing machine description

        Returns:

            str: a line equivalent to s but with transition label
                characters sorted

        """
        (prefix, remainder) = s.split(TuringMachine.labelSeparator, 1)
        (label, suffix) = remainder.split(TuringMachine.writeSymSeparator, 1)
        sortedLabel = ''.join(sorted(label))
        return prefix + TuringMachine.labelSeparator + sortedLabel \
            + TuringMachine.writeSymSeparator + suffix

    def standardizeDescription(self, d):
        """Return standardized version of the given Turing machine description.

        Args:

            d (str): A Turing machine description.

        Returns:

            str: a standardized version of d in which comments and
                whitespace and empty lines have been removed, the
                lines are sorted into lexicographical order, and
                labels have been sorted.

        """
        lines = d.split('\n')
        # remove comments
        lines = TuringMachine.stripComments(lines)
        # remove all whitespace (not just leading and trailing whitespace)
        lines = [re.sub(r'\s+', '', line) for line in lines]
        # remove empty lines
        lines = [x for x in lines if x!='']
        # sort characters within each label
        lines = [self.sortLabelChars(x) for x in lines]
        # sort
        lines.sort()
        # return single string with lines separated by newlines
        return '\n'.join(lines)
                        
    # See whether two Turing machine descriptions are the same when we
    # ignore comments, whitespace and reordering of transitions.
    def descriptionsAreSame(self, selfDesc, other, otherDesc):
        """Determine whether to Turing machine descriptions describe essentially the same machine.

        The machines are considered the same if we ignore comments,
        whitespace and reordering of transitions.

        Args:

            selfDesc (str): description of the calling Turing machine

            other (TuringMachine): the other Turing machine to be compared

            otherDesc (str): description of other

        Returns:

            bool: True if the descriptions are the same when we ignore
                comments, whitespace and reordering of transitions.

        """
        s1 = self.standardizeDescription(selfDesc)
        s2 = other.standardizeDescription(otherDesc)
        return s1 == s2


    def unifyTransitions(self):
        """Unify all transitions in this machine

        Transitions with the same source and destination state can be
        unified into a single transition with a longer label. This can
        be a useful way to simplify machine descriptions and to
        standardize them.

        """
        if self.transitions == None: return
        newTransitionsDict = dict()
        for state, tList in self.transitions.items():
            # key is tuple of all except label, value is list of labels
            tDict = dict()
            for t in tList:
                key = t.getKeyForUnify()
                labels = tDict.setdefault(key, [])
                labels.append(t.label)
            newTList = []
            for key, labels in tDict.items():
                labelStr = ''.join(labels)
                newTrans = Transition.reassembleFromUnifyKey(key, labelStr)
                newTList.append(newTrans)
            newTransitionsDict[state] = newTList
        self.transitions = newTransitionsDict

def testTransition():
    t1 = Transition('a', 'b', 'c', 'd', 'e')
    t1b = Transition('a', 'b', 'c', 'd', 'e')
    t2 = Transition('a', 'b', 'qwerty', 'd', 'e')
    t2b = Transition('a', 'b', 'xx', 'd', 'e')
    t3 = Transition('a', 'b', 'c', 'a', 'a')
    t4 = Transition('u', 'v', 'w', 'x', 'y')
    t5 = Transition.unify([t1, t2, t2b])
    t6 = Transition('a', 'b', 'cqwertyxx', 'd', 'e')

    assert t1==t1b
    assert t1!=t2
    assert t1<t2
    assert t4>t1
    assert t1.isCompatible(t1b)
    assert t1.isCompatible(t2)    
    assert not t1.isCompatible(t3)
    assert t5==t6

    utils.tprint('transitions passed tests')


def testWrite():
    testvals = ['containsGAGA.tm', 'binaryIncrementer.tm', 'shiftInteger.tm']
    for filename in testvals:
        s0 = rf(filename)
        tm1 = TuringMachine(s0)
        s1 = tm1.write()
        tm2 = TuringMachine(s1)
        s2 = tm2.write()
        utils.tprint(filename, '\n', s0, '\n\n', s1, '\n\n', s2)
        assert tm1.descriptionsAreSame(s0, tm2, s1)
        assert tm2.descriptionsAreSame(s1, TuringMachine(s2), s2)
        assert s1 == s2

def testUnifyTransitions():
    s1 = '''
q0->q1:c;x,R
q0->q1:b;x,R
q0->q1:d;x,S
q0->q1:e;y,R
q0->q1:a;x,R
q0->q0:f;x,R
q1->q0:f;x,R
q1->q0:g;x,R
'''

    s2 = '''
q0->q0:f;x,R
q0->q1:abc;x,R
q0->q1:d;x,S
q0->q1:e;y,R
q1->q0:fg;x,R
'''

    tm = TuringMachine(s1)
    tm.unifyTransitions()
    s1Unified = tm.write()
    utils.tprint(s1Unified)
    utils.tprint(s2)
    assert tm.descriptionsAreSame(s1Unified, TuringMachine(s2), s2)

def testHasSameTransitions():
    s1 = '''
q0->q0:f;x,R
q0->q1:abc;x,R
q0->q1:d;x,S
q0->q1:e;y,R
'''

    s2 = '''
q0->q0:!abcde;x,R
q0->q1:ab;x,R
q0->q1:c;x,R
q0->q1:d;x,S
q0->q1:e;y,R
q1->q2:~;R
'''
    testVals = [
        ( rf('containsGAGA.tm'), rf('containsGAGA.tm'), True),
        ( rf('binaryIncrementer.tm'), rf('binaryIncrementer.tm'), True),
        ( s1, s2, True),
        ( s2, s1, False),
    ]
    for (tm1str, tm2str, result) in testVals:
        tm1 = TuringMachine(tm1str)
        tm2 = TuringMachine(tm2str)
        val = tm1.hasSameTransitions(tm2)
        utils.tprint(val, result)
        assert val == result

# see testCheckTM() in checkTuringMachine.py for more detailed tests
def testTuringMachine():
    for (filename, inString, solution) in [
            ('containsGAGA.tm', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.tm', 'CCCGAGACCAAAAAA', 'yes'),
            # ('badCharacter.tm', 'CCCGAGACCAAAAAA'), # should throw an exception
            ('binaryIncrementer.tm', 'x100111x', 'x101000x'),
            # ('CthenGtoAthenTtoA.tm', 'GAGACCCAACCGCCTCC'),
            # ('CthenGtoAthenTtoA.tm', 'GAGACCCAACCGCCGCC'),
            # ('CthenGtoAthenTtoA.tm', 'GAGAGT'),
            # ('incrementWithOverflow.tm', 'xx0x'),
            # ('incrementWithOverflow.tm', 'xxx'),
            # ('appendZero.tm', 'xCGGGATATx'),
            # ('deleteToInteger.tm', 'xTCCGGAxx10101x'),
            ('countCs.tm', 'xGCGCGCACGCGGGx', 'x101x'),
            # ('loop.tm', 'x'),
            # ('containsGAGAorGTGT.tm', 'CCCCCCGTGTCCC'),
            ]:
        tm = TuringMachine(rf(filename), inString, keepHistory=True)
        val = tm.run()
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        utils.tprint('history:\n' + '\n'.join(tm.history) )
        assert val == solution
