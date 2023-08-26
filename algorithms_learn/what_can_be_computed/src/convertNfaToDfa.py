# SISO program convertNfaToDfa.py

# Convert an nfa into an equivalent dfa.

# inString: a string representation of an nfa

# returns: a string representation of an equivalent dfa.

# Example:
# >>> convertNfaToDfa(rf('simple1.nfa'))
# 'q0->q1: A\nq1->q2: C\nq1->q3: A\nq1->q4: G ...'
import utils; from utils import rf
from dfa import Dfa
from nfa import Nfa
from turingMachine import TuringMachine, Transition
from checkTuringMachine import checkEquivalent

def convertNfaToDfa(nfaString):
    nfa = Nfa(nfaString, name = 'sourceNfa')

    # print('source nfa is', nfa.write())

    dfa = Dfa(None, name = 'destDfa')
    # Dictionary of states in destDfa. Key is the name of the state (e.g. q0, qA),
    # and value is the set of states in sourceNfa to which the destDfa
    # state corresponds.
    stateToSubset = dict()
    # As above, but the key is the value and vice versa
    subsetToState = dict()

    # Find out where we can get to in the nfa without consuming any symbols.
    initialStateSet = getAllStayDests(nfa, set([TuringMachine.startState]))

    # If we can immediately reach the accept state, we are in the
    # special case of accepting all strings, so construct and return a
    # suitable dfa.
    if TuringMachine.acceptState in initialStateSet:
        t = Transition(TuringMachine.startState, TuringMachine.acceptState,
                       TuringMachine.anySym, None, TuringMachine.rightDir)
        dfa.addTransition(t)
        return dfa.write()

    # Begin the core algorithm by creating the first state in the dfa,
    # which corresponds to the subset of states in the NFA that can be
    # reached without consuming any symbols.
    stateToSubset[TuringMachine.startState] = initialStateSet
    subsetToState[ initialStateSet  ] = TuringMachine.startState

    # Also create an accept state
    stateToSubset[TuringMachine.acceptState] = frozenset([TuringMachine.acceptState])
    subsetToState[ frozenset([TuringMachine.acceptState])  ] = TuringMachine.acceptState
    
    # Keep track of which states in the dfa have not yet been processed
    unprocessedDfaStates = [TuringMachine.startState]

    iteration = 0 # for debugging
    while len(unprocessedDfaStates)>0:
        # print('iteration:', iteration); iteration+=1
        dfa.unifyTransitions(); # print(dfa.write())
        dfaState = unprocessedDfaStates.pop()
        nfaStates = stateToSubset[dfaState]

        # print('processing dfa state', dfaState, 'corresponding to nfa states', nfaStates)

        # 'transitions' will store transitions from dfaState.
        # key is label, value is a set of destinations
        transitions = dict()
        for c in TuringMachine.validSymbols:
            transitions[c] = set()
        for nfaState in nfaStates:
            # print('processing nfaState', nfaState)
            transitionList = nfa.getTransitions(nfaState)
            # print('transitions are', transitionList)
            for t in transitionList:
                for c in TuringMachine.validSymbols:
                    # The special anySym symbol with the 'stay'
                    # direction represents an epsilon-transition.
                    # These will be dealt with separately. For now,
                    # don't consider these to be matches.
                    if t.label==TuringMachine.anySym and \
                       t.direction == TuringMachine.stayDir:
                        continue
                    if nfa.labelMatchesSymbol(c, t.label):
                        # print(c, 'matches label', t.label)
                        if t.destState != TuringMachine.rejectState:
                            # print('adding transition with label', c, 'and dest', t.destState)
                            transitions[c].add(t.destState)
        # Expand the destinations by following all epsilon-transitions.
        # The values will now be frozensets, which is what we need.
        for c in TuringMachine.validSymbols:
            transitions[c] = getAllStayDests(nfa, transitions[c])
        # Add any new transitions to the dfa
        for label, subset in transitions.items():
            if len(subset) == 0:
                continue
            if subset not in subsetToState:
                name = getNewStateName(stateToSubset)
                stateToSubset[name] = subset
                subsetToState[subset] = name
                unprocessedDfaStates.append(name)
            else:
                name = subsetToState[subset]
            tr = Transition(dfaState, name, label, None, TuringMachine.rightDir)
            dfa.addTransition(tr)

    # not strictly necessary, but makes the representation easier to test
    dfa.unifyTransitions()

    return dfa.write()
                
            
        
    
    

# Return a frozenset of all possible destination states leading from
# subset of states qSet in the given nfa, where we can reach the
# destination without consuming a symbol.  (Exception: if the accept
# state can be reached without consuming a symbol, then a singleton
# containing only the accept state is returned.) We call of the
# resulting set of states the "stayDests". Effectively, we are asking
# to follow all the epsilon-transitions. But because the nfa is stored
# in an underlying format as a Turing machine, we in fact look for
# destinations that follow a transition and do not move the head to
# the right. By definition, the given state q is in the set of
# stayDests, and then we must iteratively define the set as all other
# states that can be reached from any state in the current set without
# consuming a symbol.
def getAllStayDests(nfa, qSet):
    stayDests = {q for q in qSet}
    frontier = {q for q in qSet}
    while not len(frontier)==0:
        newFrontier = set()
        for state in frontier:
            transitionList = nfa.getTransitions(state)
            newStayDests = set([t.destState for t in transitionList if t.direction == TuringMachine.stayDir])
            # transitions to the reject state are ignored in this algorithm
            if TuringMachine.rejectState in newStayDests:
                newStayDests.remove(TuringMachine.rejectState)
            newFrontier = newFrontier | (newStayDests - stayDests)
            stayDests = stayDests | newStayDests
        frontier = newFrontier
    # As stated above, the accept state is a special case -- if we can
    # reach it, return a singleton containing only the accept state.
    if TuringMachine.acceptState in stayDests:
        return frozenset([TuringMachine.acceptState])
    else:
        return frozenset(stayDests)

def getNewStateName(states):
    i = 0
    while True:
        name = 'q' + str(i)
        if name not in states:
            return name
        i += 1
    
def testGetAllStayDests():
    treeOfEpsNfaStr = """
q0->q1 : Eps
q1->q2 : Eps
q2->q3 : Eps
q3->q4 : Eps
q2->q5 : Eps
q2->q6 : Eps
"""
    multiChainOfEpsNfaStr = """
q0->q1 : Eps
q1->q2 : Eps
q3->q4 : Eps
q5->q6 : Eps
"""

    cycleOfEpsNfaStr = """
q0->q1 : Eps
q1->q2 : Eps
q2->q3 : Eps
q3->q4 : Eps
q4->q0 : Eps
"""

    chainWithAccept = """
q0->q1 : Eps
q1->q2 : Eps
q2->qA : Eps
"""

    nfaTree = Nfa(treeOfEpsNfaStr)
    nfaCycle = Nfa(cycleOfEpsNfaStr)
    nfaAccept = Nfa(chainWithAccept)
    nfaMulti = Nfa(multiChainOfEpsNfaStr)
    nfa1 = Nfa(rf('example2.nfa'))
    nfa2 = Nfa(rf('mult2or3Gs.nfa'))
    testvals = [
        (nfa1, set(['q0']), frozenset(['q0'])  ),
        (nfa1, set(['q1']), frozenset(['q1', 'q2'])  ),
        (nfa2, set(['q0']), frozenset(['q0', 'q1', 'q3'])  ),
        (nfaTree, set(['q0']), frozenset(['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'])  ),
        (nfaTree, set(['q1']), frozenset(['q1', 'q2', 'q3', 'q4', 'q5', 'q6'])  ),
        (nfaCycle, set(['q0']), frozenset(['q0', 'q1', 'q2', 'q3', 'q4'])  ),
        (nfaCycle, set(['q1']), frozenset(['q0', 'q1', 'q2', 'q3', 'q4'])  ),
        (nfaAccept, set(['q0']), frozenset(['qA'])  ),
        (nfaMulti, set(['q0']), frozenset(['q0', 'q1', 'q2'])  ),
        (nfaMulti, set(['q2']), frozenset(['q2'])  ),
        (nfaMulti, set(['q1', 'q5']), frozenset(['q1', 'q2', 'q5', 'q6'])  ),
        (nfaMulti, set(['q0', 'q3', 'q5']), frozenset(['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'])  ),
    ]
    for ( nfa, state, solution) in testvals:
        val = getAllStayDests(nfa, state)
        utils.tprint(state, ':', val)
        assert val == solution

import checkTuringMachine

NUM_BRIEF_TESTS = 3


        
def testConvertNfatoDfa():
    testvals = [
        # format is:
        #(nfaFile, alphabet, maxShortInputLen, maxRandInputLen, numRandInputs)
        ('chainWithAccept.nfa', 'abc', 4, 20, 100),
        ('CGstar.nfa', 'CAGT', 5, 20, 100),
        ('simple1.nfa', 'CAGT', 6, 12, 1000),
        ('simple2.nfa', 'CAGT', 6, 12, 10000),
        ('simple3.nfa', 'CAGT', 6, 12, 10000),
        ('mult2or3Gs.nfa', 'G', 10, 50, 1000),
        ('example2.nfa', 'CAGT', 9, 20, 10000),
    ]
    numTests = 0;
    for (nfaFile, alphabet, maxShortInputLen, maxRandInputLen, numRandInputs) in testvals:
        numTests += 1
        if utils.BRIEF_TESTS and numTests > NUM_BRIEF_TESTS: break
        nfaStr = rf(nfaFile)
        nfa = Nfa(nfaStr)
        dfaStr = convertNfaToDfa(nfaStr)
        utils.tprint('\n'.join(['nfaStr', nfaStr, '\ndfaStr', dfaStr]))
        checkEquivalent(dfaStr, nfa, alphabet, maxShortInputLen, maxRandInputLen, \
                        numRandInputs, tmType = 'dfa')
        
