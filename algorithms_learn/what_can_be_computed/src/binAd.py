"""Module for working with the binAd logical system.
"""

import utils; from utils import rf
import re

theAxiom = '1=1'
"""The only axiom for the binAd system"""


binaryNumRegexString = r'[01]+'
binaryNumRegex = re.compile(binaryNumRegexString)

wellFormedRegexString = r'^[01]+(\+[01]+)*=[01]+(\+[01]+)*$'
wellFormedRegex = re.compile(wellFormedRegexString)

ruleTwoRegexString = r'([=+]|^)([01]+)(?=\+\2([=+]|$))'
ruleTwoRegex = re.compile(ruleTwoRegexString)
NRuleTwoGroupID = 2

ruleThreeRegexString = r'([=+]|^)1\+([01]+)0([=+]|$)'
ruleThreeRegex = re.compile(ruleThreeRegexString)
NRuleThreeGroupID = 2

def isWellFormed(f):
    """Return True if f is well formed and False otherwise.

    Args:
    
        f (str): string representing a possible formula in binAd

    Returns: 

        bool: True if f is well formed and False otherwise.

    """
    if wellFormedRegex.match(f):
        return True
    else:
        return False

def testIsWellFormed():
    testvals = [('', False),
                ('1', False),
                ('1=2', False),
                ('=101', False),
                ('101=', False),
                ('111==11', False),
                ('1+1+=101', False),
                ('1=1', True),
                ('1=0', True),
                ('101111=111000', True),
                ('101+1+0101=1111+1+0+1', True),
            ]
    for (inString, solution) in testvals:
        val = isWellFormed(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

def applyRuleOne(f):
    """Apply Rule 1 to the formula f.

    Args:
    
        f (str): string representing a formula in binAd

    Returns: 

        set of str: Set of formulas that can be produced by applying
           Rule 1 to f. This will be empty if f is not well formed.

    """
    result = set()
    if not isWellFormed(f):
        return result
    (lhs,rhs) = f.split('=')
    newF = '1+' + lhs + '=' + '1+' + rhs
    result.add(newF)
    return result

def testApplyRuleOne():
    testvals = [('',set()),
                ('1',set()),
                ('1=2',set()),
                ('=101',set()),
                ('101=',set()),
                ('111==11',set()),
                ('1+1+=101',set()),
                ('1=1',set(['1+1=1+1',])),
                ('1=0',set(['1+1=1+0',])),
                ('101111=111000',set(['1+101111=1+111000',])),
                ('101+1+0101=1111+1+0+1',set(['1+101+1+0101=1+1111+1+0+1',])),
    ]
    for (inString, solution) in testvals:
        val = applyRuleOne(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

def applyRuleTwo(f):
    """Apply Rule 2 to the formula f.

    Args:
    
        f (str): string representing a formula in binAd

    Returns: 

        set of str: Set of formulas that can be produced by applying
           Rule 2 to f. This will be empty if f is not well formed.

    """
    result = set()
    if not isWellFormed(f):
        return result
    
    for m in ruleTwoRegex.finditer(f):
        N = m.group(NRuleTwoGroupID)
        assert binaryNumRegex.match(N)
        Nstart = m.start(NRuleTwoGroupID)
        Nend = m.end(NRuleTwoGroupID)
        Nlen = Nend - Nstart
        newN = N + '0'
        replaceLen = 2*Nlen + 1 # ``N+N'' is the string being replaced, so its length is 2*Nlen+1
        newF = f[:Nstart] + newN + f[Nstart+replaceLen:]
        result.add(newF)

    return result
    
def testApplyRuleTwo():
    testvals = [('', set() ), 
                ('1', set() ),
                ('1=1', set() ),
                ('1+1', set() ),
                ('1+1=10', set(['10=10']) ),
                ('1+1+1+1=10+10', set(['10+1+1=10+10','1+10+1=10+10','1+1+10=10+10','1+1+1+1=100']) ),
                ('1+1+11+101+101+11=11+11+11+1+1', set(['10+11+101+101+11=11+11+11+1+1', '1+1+11+1010+11=11+11+11+1+1', '1+1+11+101+101+11=110+11+1+1', '1+1+11+101+101+11=11+110+1+1', '1+1+11+101+101+11=11+11+11+10']) ),
            ]
    for (inString, solution) in testvals:
        val = applyRuleTwo(inString)
        utils.tprint(inString, ':', val)
        assert val == solution


def applyRuleThree(f):
    """Apply Rule 3 to the formula f.

    Args:
    
        f (str): string representing a formula in binAd

    Returns: 

        set of str: Set of formulas that can be produced by applying
           Rule 3 to f. This will be empty if f is not well formed.

    """
    result = set()
    if not isWellFormed(f):
        return result
    
    for m in ruleThreeRegex.finditer(f):
        N = m.group(NRuleThreeGroupID)
        assert binaryNumRegex.match(N)
        Nstart = m.start(NRuleThreeGroupID)
        Nend = m.end(NRuleThreeGroupID)
        Nlen = Nend - Nstart
        newN = N + '1'
        replaceLen = Nlen + 3 # ``1+N0'' is the string being replaced, so its length is Nlen+3
        replaceStart = Nstart-2 # start replacing 2 chars before N, i.e., at the ``1'' in ``1+N0''
        newF = f[:replaceStart] + newN + f[replaceStart+replaceLen:]
        result.add(newF)

    return result
    
def testApplyRuleThree():
    testvals = [('', set() ),
                ('1',  set() ),
                ('1+10',  set() ),
                ('1+10=11',  set(['11=11',]) ),
                ('1+10+1+10101+1+1010=1+1+100', set(['11+1+10101+1+1010=1+1+100', '1+10+1+10101+1011=1+1+100', '1+10+1+10101+1+1010=1+101']) ),
    ]
    for (inString, solution) in testvals:
        val = applyRuleThree(inString)
        utils.tprint(inString, ':', val)
        assert val == solution


def applyAllRules(f):
    """Apply Rules 1, 2, and 3 to the formula f.

    Args:
    
        f (str): string representing a formula in binAd

    Returns: 

        set of str: Set of formulas that can be produced by applying
           Rule 1 or 2 or 3 to f. This will be empty if f is not well
           formed.

    """

    # Note that ``|'' is the set union operator in Python, so the
    # following statement returns the union of three sets.
    return applyRuleOne(f) | applyRuleTwo(f) | applyRuleThree(f)

def testApplyAllRules():
    testvals = [('', set() ), 
                ('1', set() ), 
                ('1+10', set() ), 
                ('1+10=11', set(['1+1+10=1+11', '11=11']) ), 
                ('1+10+1+10101+1+1010=1+1+100', set(['1+1+10+1+10101+1+1010=1+1+1+100', '1+10+1+10101+1+1010=10+100', '11+1+10101+1+1010=1+1+100', '1+10+1+10101+1011=1+1+100', '1+10+1+10101+1+1010=1+101']) ),
    ]
    for (inString, solution) in testvals:
        val = applyAllRules(inString)
        utils.tprint(inString, ':', val)
        assert val == solution


def applyAllRulesToFrontier(provedFormulas, frontierFormulas, predecessors = None):
    """Apply Rules 1, 2, and 3 to a set of frontier formulas.

    This function will apply all inference rules to the frontier,
    adding any newly proved formulas to provedFormulas and returning a
    new frontier consisting of only the newly proved formulas. A
    dictionary of predecessor formulas, if given, is also updated.

    Args:
    
        provedFormulas (set of str): a set of formulas that have been
            proved already. Formulas in this set may or may not have
            yet been used to generate new formulas via inference
            rules. This set will be updated, producing a set that
            includes all newly proved formulas.

        frontierFormulas (set of str): set of formulas to which the
            inference rules have not yet been applied.  By definition,
            frontierFormulas is a subset of provedFormulas and the
            function will produce an assertion failure if this is not
            the case.

        predecessors (dict mapping str to str): dictionary in which
            the key is a formula f and the value is a formula f' which
            was used to generate f via an inference rule. This
            parameter is optional, but if it exists, this dictionary
            will be updated.

    Returns: 

        set of str: a new frontier consisting of only the newly proved
            formulas.

    """
    assert frontierFormulas <= provedFormulas
    newFrontier = set()
    # the ``sorted'' below is not needed for correctness, but is
    # needed to obtain same predecessors every time (there is
    # otherwise ambiguity in the definition)
    for f in sorted(frontierFormulas):
        newFs = applyAllRules(f)
        newFrontier |= newFs
        if predecessors:
            # the ``sorted'' below is not needed for correctness, but is
            # needed to obtain same predecessors every time (there is
            # otherwise ambiguity in the definition)
            for newF in sorted(newFs): 
                if newF not in predecessors:
                    predecessors[newF] = f
    alreadyProved = newFrontier & provedFormulas
    newFrontier -= alreadyProved
    provedFormulas |= newFrontier
    return newFrontier
    
def testApplyAllRulesToFrontier():
    provedFormulas = set([theAxiom])
    frontierFormulas = provedFormulas
    utils.tprint()
    utils.tprint('provedFormulas:', provedFormulas)
    utils.tprint('frontierFormulas:', frontierFormulas)
    solutions = [ # format is (provedFormulas, frontierFormulas)
        (set(['1+1=1+1', '1=1']), set(['1+1=1+1'])), 
        (set(['1+1=1+1', '1=1', '10=1+1', '1+1+1=1+1+1', '1+1=10']), set(['10=1+1', '1+1+1=1+1+1', '1+1=10'])), 
        (set(['1=1', '1+1+1+1=1+1+1+1', '1+1+1=1+1+1', '1+1=1+1', '1+10=1+1+1', '1+1=10', '1+1+1=1+10', '10=10', '10+1=1+1+1', '1+1+1=10+1', '10=1+1']), set(['1+10=1+1+1', '1+1+1=1+10', '10=10', '10+1=1+1+1', '1+1+1=10+1', '1+1+1+1=1+1+1+1'])), 
    ]
    for i in range(3):
        frontierFormulas = applyAllRulesToFrontier(provedFormulas, frontierFormulas)
        utils.tprint()
        utils.tprint('provedFormulas:', provedFormulas)
        utils.tprint('frontierFormulas:', frontierFormulas)
        assert provedFormulas == solutions[i][0]
        assert frontierFormulas == solutions[i][1]


def testApplyAllRulesToFrontierWithPredecessors():
    provedFormulas = set([theAxiom])
    frontierFormulas = provedFormulas
    predecessors = {theAxiom: ''}
    utils.tprint()
    utils.tprint('predecessors:', predecessors)
    solutions = [ # only check predecessors. others checked in previous test.
        {'1+1=1+1': '1=1', '1=1': ''},
        {'1+1+1=1+1+1': '1+1=1+1', '1+1=1+1': '1=1', '1+1=10': '1+1=1+1', '10=1+1': '1+1=1+1', '1=1': ''},
        {'1=1': '', '1+1+1=1+10': '1+1+1=1+1+1', '1+1+1+1=1+1+1+1': '1+1+1=1+1+1', '1+10=1+1+1': '1+1+1=1+1+1', '1+1=10': '1+1=1+1', '10=1+1': '1+1=1+1', '1+1=1+1': '1=1', '10=10': '1+1=10', '1+1+1=1+1+1': '1+1=1+1', '1+1+1=10+1': '1+1+1=1+1+1', '10+1=1+1+1': '1+1+1=1+1+1'},
    ]
    for i in range(3):
        frontierFormulas = applyAllRulesToFrontier(provedFormulas, frontierFormulas, predecessors)
        utils.tprint()
        utils.tprint('predecessors:', predecessors)
        if predecessors != solutions[i]:
            utils.tprint('ERROR')
            utils.tprint('predecessors: ', predecessors)
            utils.tprint('solutions[i]: ', solutions[i])
            d = DictDiffer(predecessors, solutions[i])
            d.printAllChanges()
            
        assert predecessors == solutions[i]


def getProofFromPredecessors(f, predecessors):
    """Generate a proof of the formula f.

    This function generates a proof of the binAd formula f, given a
    dictionary information about formulas' predecessors i.e. what a
    given formula could have been derived from using an inference
    rule. For reasons of practicality, we limit proofs to a length of
    1000.

    Args:
    
        f (str): string representing a formula in binAd

        predecessors (dict mapping str to str): dictionary in which
            the key is a formula f and the value is a formula f' which
            was used to generate f via an inference rule. Typically
            this would have been constructed using calls to
            applyAllRulesToFrontier().

    Returns: 

        list of str: a sequence of formulas that constitute a proof of
            f.

    """
    
    maxPredecessors = 1000
    proof = [f]
    predecessor = predecessors[f]
    count = 0
    while predecessor != '' and count <= maxPredecessors:
        proof.append(predecessor)
        predecessor = predecessors[predecessor]
        count = count + 1
    if count > maxPredecessors:
        print ('Warning: unexpected loop or long chain of predecessors:')
        print(proof)
    proof.reverse()
    return proof

def enumerateStatements(K):
    """Generate at least K provable statements and return them as a set.

    Args:
    
        K (int): a lower bound on the number of provable statements
            that will be generated.

    Returns: 

        set of str: a set of provable statements.

    """
    proved = set([theAxiom])
    frontier = proved
    while len(proved) < K:
        frontier = applyAllRulesToFrontier(proved, frontier)
    return proved

def testEnumerateStatements():
    solution = {'1+1+1=1+10', '10+1=1+1+1', '10=10', '1+1=10', '10=1+1', '1+1+1+1=1+1+1+1', '1=1', '1+1=1+1', '1+1+1=10+1', '1+1+1=1+1+1', '1+10=1+1+1'}
    val = enumerateStatements(10)
    utils.tprint(val)
    assert val == solution

        
def isProvable(f, maxFormulas = 100000):
    """Attempt to determine whether f is provable and return a proof if one is found.

    Args:
    
        f (str): string representing a formula in binAd

        maxFormulas (int): an (approximate) upper bound on the number
            of provable statements that will be generated while trying
            to prove f.

    Returns: 

        (str, list of str): a 2-tuple (result, proof), where

            result: is a string describing what happened, e.g., ``not
            well-formed...'' or ``provable'' or ``not proved...''. 

            proof: is an ordered list of the formulas used to prove f.
                If no proof was found, proof is None.

    """
    proof = None
    if not isWellFormed(f):
        result = 'not well-formed, therefore not provable'
    else:
        proved = set([theAxiom])
        frontier = proved
        predecessors = {theAxiom: ''}
        while len(proved)<maxFormulas:
            frontier = applyAllRulesToFrontier(proved, frontier, predecessors)
            if f in proved:
                break
        if f in proved:
            result = 'provable'
            proof = getProofFromPredecessors(f, predecessors)
        else:
            result = 'not proved in first ' + str(len(proved)) + ' formulas generated'
    return (result, proof)

def testIsProvable():
    testvals = [
        ('1', 'not'),
        ('1=1', 'provable'),
        ('10=10', 'provable'),
        ('1+1=10', 'provable'),
        # ('1+10+10+1=110', 'provable'),  # requires approx 10000 formulas
        ('1+1+1=1+1+1+1', 'not'),
        ('1+1=1+1+1', 'not'),
        ('1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1=11000', 'not'),
    ]
    for (inString, solution) in testvals:
        (result, proof) = isProvable(inString, 2000)
        utils.tprint(inString, ':', result)
        if result == 'provable':
            utils.tprint('proof:', proof)
        assert result.startswith(solution)


def computeBinarySum(s):
    """Compute a sum of binary numbers from a string expression

    Args:
    
        s (str): string representing a sum of binary numbers,
            e.g. '101+1+10011'

    Returns: 

        int: the sum of the binary numbers in s

    """
    nums = [int(x,2) for x in s.split('+')]
    return sum(nums)

def testComputeBinarySum():
    testvals = [
        ('1', 1),
        ('0', 0),
        ('10', 2),
        ('01', 1),
        ('1+1', 2),
        ('101+1+10011', 25),
        ('1+11+111+1111+11111', 57),
    ]
    for (inString, solution) in testvals:
        val = computeBinarySum(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

def isTrue(f):
    """Return True if f is a true BinAd formula and False otherwise.

    Args:
    
        f (str): string representing a formula in binAd

    Returns: 

        bool: True if f is a true BinAd formula and False otherwise

    """
    if not isWellFormed(f):
        return False
    (lhs,rhs) = f.split('=')
    leftSum = computeBinarySum(lhs)
    rightSum = computeBinarySum(rhs)
    return (leftSum == rightSum)

def testIsTrue():
    testvals = [
        ('', False),
        ('123=321', False),
        ('1', False),
        ('1=1', True),
        ('10=10', True),
        ('1+1=10', True),
        ('1+10+10+1=110', True),
        ('1+1+1=1+1+1+1', False),
        ('1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1=11000', True),
    ]
    for (inString, solution) in testvals:
        val = isTrue(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

def isProof(proof, target):
    """Determine whether a proof is a correct mechanical proof of a given target statement.

    Note that this function returns a string ('yes' or 'no'), not a Boolean.

    Args:
    
        proof (str): A string representing a proof in binAd. The
            statements in the proof are separated by whitespace.

        target (str): string representing a formula in binAd,
            purportedly the target of the proof. That is, we are
            trying to determine whether the given proof does indeed
            prove the target statement.

    Returns: 

        str: 'yes' if the parameter proof is a mechanical proof of the
            target formula, and 'no' otherwise

    """

    # split proof into lines, stripping whitespace and removing empty lines
    proofLines = [x.strip() for x in proof.split()]
    proofLines = [x for x in proofLines if x!='']

    # strip whitespace from target
    target = target.strip()

    # check that each line of the proof is well formed
    for statement in proofLines:
        if not isWellFormed(statement):
            return 'no'

    # check that the last line of the proof is the same as the target
    if proofLines[-1] != target:
            return 'no'

    # check that each line of the proof follows from an earlier line
    for i in range(len(proofLines)):
        statement = proofLines[i]
        statementProved = False

        # Is the current statement an axiom?
        if statement == theAxiom:
            statementProved = True
        # Otherwise, this statement must be proved from an earlier
        # statement. 
        else:
            # Step backwards through the proof looking for an earlier
            # statement that implies the current statement. The
            # quadratic cost of this approach could be improved, but
            # it's good enough for our purposes.
            for j in range(i-1,-1,-1):
                prevStatement = proofLines[j]
                results = applyAllRules(prevStatement)
                if statement in results:
                    statementProved = True
                    break
            if not statementProved:
                return 'no'
    return 'yes'
            
def testIsProof():
    goodProof1 = """
1=1
1+1=1+1
1+1+1=1+1+1
1+1+1=1+10
1+1+1=11
10+1=11
"""

    goodProof2 = """
1=1
1+1=1+1
1=1
1+1+1=1+1+1
1+1+1=1+10
1+1+1=11
1+1+1+1=1+1+1+1
1+10=1+10
10+1=11
"""
    badProof1 = """
1=1
1+1=1+1
1+1+1=1+1+1
1+1+1=11
10+1=11
"""

    badProof2 = """
asdfsa
dfd
10+1=11
"""

    badProof3 = """
1=1
1+1=1+1
1+1+1=1+1+1
1+1+1=1+10
1+1+1=11
"""
    
    target = '10+1=11'
    testvals = [
        (goodProof1, 'yes'),
        (goodProof2, 'yes'),
        (badProof1, 'no'),
        (badProof2, 'no'),
        (badProof3, 'no'),
    ]
    for (inString, solution) in testvals:
        val = isProof(inString, target)
        utils.tprint(inString, target, ':', val)
        assert val == solution



# from http://stackoverflow.com/questions/1165352/calculate-difference-in-keys-contained-in-two-python-dictionaries/1165552#1165552
# author is hughdbrown?, http://stackoverflow.com/users/10293/hughdbrown
# with slight edit by jmac
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def changedWithVals(self):
        return set((o,self.past_dict[o],self.current_dict[o]) for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
    def printAllChanges(self):
        print('added:', self.added())
        print('removed:', self.removed())
        print('changed:', self.changedWithVals())
        
