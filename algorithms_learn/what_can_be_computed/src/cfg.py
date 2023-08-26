import utils; from utils import rf

class Rule:
    """Models a rule in a context free grammar.

    Rules have a left-hand side in a right-hand side. The left-hand
    side represents a non-terminal in the grammar. The right-hand side
    is a sequence of zero or more symbols. The meaning of the rule is
    that the left-hand side can be converted into the right-hand side
    as part of a derivation of a string.

    """
    
    def __init__(self, lhs, rhs):
        """Initialize Rule object.

        Args:

            lhs (str): a single character, which is the non-terminal
            on the left-hand side of this rule

            rhs (str): the sequence of symbols on the right-hand side
                of this rule. It can be the empty string.

        """
        # lhs is a single character, which is the non-terminal on the
        # left-hand side of this rule
        self.lhs = lhs
        # a string, which is the sequence of symbols on the right-hand
        # side of this rule (and can be the empty string)
        self.rhs = rhs

    def __str__(self):
        return 'lhs: %s rhs: %s' % \
            (self.lhs, self.rhs)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self is other: return True
        if other==None: return False
        if not isinstance(other, type(self)): return False
        return (self.lhs, self.rhs) == (other.lhs, other.rhs)

    def __ne__(self, other):
        return not self==other

class Cfg:
    """Represents a context free grammar.

    """
    
    commentStart = '#'
    ruleSeparator = '->'
    alternativeSep = '|'
    startSymbol = 'S'
    epsilonStr = 'Eps'

    def __init__(self, description = None):
        """Initialize Cfg object.

        Args:

            description (str, optional): A string describing the rules
                of the grammar. See the read() method for
                documentation of the format.

        """

        self.rules = None
        """dict mapping str to list of Rules.

        In this dictionary, a key is a variable V in the grammar. The
        corresponding value is a list of Rule objects, containing all
        rules whose left-hand side is the variable V.

        """
        
        self.variables = None
        """frozenset containing all variables in the grammar."""
        
        self.accepted = set()
        """A set of strings known to be in the language of this cfg."""


        # Keys are a set of sentential forms that have not yet had
        # rules applied to them. For a given key, value is the
        # sentential form from which it was derived.
        self.frontier = dict()
        """dict mapping str to str.

        In this dictionary, a key is a sentential form S that has been
        derived at some point earlier but has not yet had rules
        applied to it. The corresponding value is the sentential form
        S' from which S was derived. For the particular case of the
        start symbol, S' is the empty string.

        """
        
        # Initialize the frontier with the start symbol.
        self.frontier[Cfg.startSymbol] = ''

        self.explored = dict()
        """dict mapping str to str.

        In this dictionary, a key is a sentential form S that has been
        derived at some point earlier and has already had rules
        applied to it. The corresponding value is the sentential form
        S' from which S was derived. For the particular case of the
        start symbol, S' is the empty string.

        """
        
        if description:
            self.read(description)
        

    def read(self, description):
        """Initialize the rules of the grammar based on an ASCII description.

        This method initializes both the self.rules attribute and the
        self.variables attribute.

        Args:

            description (str): A string describing the rules of the
                grammar. Each rule should appear in a separate line of
                the string, except that as usual for context free
                grammars, rules with the same left-hand side can be
                combined using '|' on the right-hand side. Comments
                can be prefixed with #. The left-hand side and
                right-hand side of a rule are separated by '->'. The
                start symbol is 'S' and the empty string is
                represented by 'Eps'. Whitespace will be ignored in
                most places.

        """

        self.rules = dict()
        # split on newlines
        lines = description.split('\n')
        # strip comments (anything after a Cfg.commentStart)
        lines = [x.split(Cfg.commentStart)[0] for x in lines]        
        # strip whitespace
        lines = [x.strip() for x in lines]
        for line in lines:
            if len(line)>0:
                r = self.extractRules(line)
                rulesList = self.rules.setdefault(r[0].lhs, [])
                rulesList.extend(r)
        self.variables = frozenset(self.rules.keys())

    def splitRule(self, line):
        """Split a given line of a grammar description into rule strings.

        Args:

            line (str): A line in a grammar description (see the
                read() method for details.)

        Returns:

            (str, list of str): A 2-tuple (lhs, rhsides) where lhs is
                the left-hand side of the rule and rhsides is a list
                of all the right-hand side were present -- there can
                be more than one of these, separated by '|'.

        """
        (lhs, rhsides) = [x.strip() for x in line.split(Cfg.ruleSeparator)]
        rhsides = [x.strip() for x in rhsides.split(Cfg.alternativeSep)]
        return (lhs, rhsides) 

    def extractRules(self, line):
        """Extract Rule objects from a given line of a grammar description.

        Args:

            line (str): A line in a grammar description (see the
                read() method for details.)

        Returns:

            list of Rule objects: Each rule in this list represents
                one of the rules present in the input -- there may
                have been more than one of these, separated by '|'.

        """
        (lhs, rhsides) = self.splitRule(line)
        ruleList = []
        for rhs in rhsides:
            if rhs == Cfg.epsilonStr:
                rhs = ''
            newRule = Rule(lhs, rhs)
            ruleList.append(newRule)
        return ruleList

    def printRules(self):
        """Print the rules of the grammar via utils.tprint().

        This is primarily intended for debugging and testing.
        """
        utils.tprint('variables:', self.variables)
        utils.tprint('rules:')
        for r in self.rules.values():
            utils.tprint(r)

    def printAccepted(self):
        """Print the accepted strings of the grammar via utils.tprint().

        This is primarily intended for debugging and testing. The
        accepted strings are printed in shortlex order.

        """

        # Print in shortlex order. Therefore, sort first
        # alphabetically, then by length.
        accepted = sorted(self.accepted)
        accepted = sorted(accepted, key=len)
        utils.tprint('accepted:', accepted)

    def printAllStrings(self):
        """Print the all relevant sentential forms of the grammar via utils.tprint().

        This is primarily intended for debugging and testing. 

        """
        self.printAccepted()
        utils.tprint('explored:', self.explored)
        utils.tprint('frontier:', self.frontier)
        

    # apply all rules to the given string s, returning a list of the
    # resulting strings
    def applyRulesToString(self, s):
        """Apply all rules of the grammar to a given string.

        Args:

            s (str): A sentential form.

        Returns:

            list of str: A list of all sentential forms that can be
                produced by the action of a single rule of grammar on
                s.

        """
        results = []
        for i in range(len(s)):
            c = s[i]
            if c in self.variables:
                rules = self.rules[c]
                for r in rules:
                    prefix = s[:i]
                    suffix = s[i+1:]
                    result = prefix + r.rhs + suffix
                    results.append(result)
        return results
                

    def applyRulesToFrontier(self):
        """Update the frontier by applying all rules of the grammar to it.

        This method updates self.frontier. For every sentential form
        in the current frontier, we apply all rules of the
        grammar. Any results that have not already been explored are
        placed into the new version of self.frontier.

        """
        newFrontier = dict()
        for s in self.frontier:
            results = self.applyRulesToString(s)
            for result in results:
                if result in self.explored or result in self.frontier:
                    pass
                else:
                    if self.containsVariable(result):
                        newFrontier[result] = s
                    else:
                        self.accepted.add(result)
        for (s, predecessor) in  self.frontier.items():
            assert s not in self.explored
            self.explored[s] = predecessor
        self.frontier = newFrontier


    def containsVariable(self, s):
        """Determine whether a string contains a variable i this grammar

        Args:

            s (str): A sentential form.

        Returns:

            bool: True if s contains one of the grammar's variables,
            and False otherwise.

        """
        for v in self.variables:
            if v in s: return True
        return False

    def removeLongStringsFromFrontier(self, maxLen):
        """Update the frontier by removing all sufficiently long strings.

        This can be necessary for practical reasons, especially for testing.

        Args:

            maxLen (int): Strings longer than this will be removed.

        """
        victims = []
        for s in self.frontier:
            if len(s)>maxLen:
                victims.append(s)
        for v in victims:
            del self.frontier[v]

    def generateLanguage(self, maxLen = 50, maxDepth = 50, maxStrings = 100000):
        """Generate some of the strings in the language of the grammar.

        Generate some of the strings in the language, using breadth
        first application of all rules. Nothing is returned, but the
        results are stored in self.accepted.


        Args:

            maxLen (int): The maximum length of a sentential form that
                can be used in a derivation. This is NOT the maximum
                length of a string of terminals generated -- it's an
                upper bound on that, but if a short string can only be
                derived from a very long sentential form, we would
                never generate the short string.

            maxDepth (int): Maximum depth of the parse tree (i.e.,
                maximum length of the derivation).

            maxStrings (int): The (approximate) maximum number of
                strings in the language that will be generated. It is
                approximate because we stop after generating no less
                than maxStrings, assuming the other termination
                criteria didn't kick in first.

        """

        depth = 0
        done = False
        while not done:
            depth += 1
            self.applyRulesToFrontier()
            self.removeLongStringsFromFrontier(maxLen)
            if len(self.frontier)==0 or depth>=maxDepth \
               or len(self.accepted)>=maxStrings:
                done = True
            
    
def testCfg():
    cfg = Cfg(rf('GnTn.cfg'))

    rules = {'S': [Rule('S',''), Rule('S', 'GST')]}
    assert cfg.rules == rules

    cfg.printRules()
    # for i in range(10):
    #     utils.tprint('\nApplying rules, iteration', i, '...')
    #     cfg.applyRulesToFrontier()
    #     cfg.printAllStrings()
    cfg.generateLanguage(2000, 1000, 20)
    cfg.printAllStrings()

    for length in range(6):
        assert 'G'*length + 'T'*length in cfg.accepted

    for s in cfg.accepted:
        assert len(s)%2 == 0
        halfLen = int(len(s)/2)
        for c in s[:halfLen]: assert c== 'G'
        for c in s[halfLen:]: assert c== 'T'


