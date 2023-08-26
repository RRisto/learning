# SISO program simulate2TDCM.py

# Simulate a given 2TDCM with a given input. This is not quite a
# genuine SISO program because we allow an optional boolean parameter,
# but this can be ignored.

# simulate2TDCM.py is provided as a self-contained implementation of a
# Turing machine simulator using only elementary Python.  Note that
# the book materials also provide a more sophisticated and robust
# 2TDCM simulator called twoTDCM.py. However, that simulator uses
# object-oriented Python, which requires additional effort to
# understand.

# tmString: ASCII description of the 2TDCM to be simulated

# inString: the initial content of the machine's tape

# verbose: optional boolean indicating whether extra output should be printed

# returns: As discussed in the book, a "good" 2TDCM runs forever. In
# practice, this implementation returns a message stating the outcome
# and final tape contents when either a maximum number of steps are
# completed or the machine becomes "stuck" (i.e. enters a halting
# state).

# Example:
# >>> simulate2TDCM(rf('unarySequence.tm'), '')
# 'exceeded maxSteps, outTape is:0010110111011110111110111111011111110...
import utils; from utils import rf
from turingMachine import TuringMachine
import re
def simulate2TDCM(tmString, inString, verbose = False):
    # key is state, value is list of transitions
    transitions = dict()
    tmLines = [x.strip() for x in tmString.split('\n')]
    splitRegex = '[' + \
                 TuringMachine.labelSeparator + \
                 TuringMachine.writeSymSeparator + \
                 ']'
    for line in tmLines:
        if len(line)>0:
            (states, label, actions) = [x.strip() for x in re.split(splitRegex,line)]
            (sourceState, destState) = [x.strip() for x in states.split(TuringMachine.stateSeparator)]
            if TuringMachine.actionSeparator in actions:
                (writeSymbol, direction) = actions.split(TuringMachine.actionSeparator)
            else:
                (writeSymbol, direction) = (None, actions)
            transitionList = transitions.setdefault(sourceState, [])
            transitionList.append( (destState, label, writeSymbol, direction) )

    # Recall that in a 2TDCM, there is a ``regular'' tape and an ``output''
    # tape.  There is no need to keep track of the head position on the
    # output tape, because we always append to that tape, and we never
    # read it.
    regTape = [c for c in inString]
    regHeadPos = 0
    outTape = [ ]
    # Also recall that in a 2TDCM, only the symbols 0-9 can be written
    # on the output tape.
    outSymbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    state = TuringMachine.startState
    stuck = False
    steps = 0
    maxSteps = 1000

    while not stuck and steps < maxSteps:
        steps = steps + 1
        if verbose: print(steps, regTape, regHeadPos, outTape)
        if regHeadPos == len(regTape):
            regTape.append(TuringMachine.blank)
        scannedSymbol = regTape[regHeadPos]
        transitionList = transitions[state]
        foundTransition = False
        for (destState, label, writeSymbol, direction) in transitionList:
            if TuringMachine.anySym == label:
                foundTransition = True
                break
            elif label[0] == TuringMachine.notSym:
                if scannedSymbol not in label[1:]: 
                    foundTransition = True
                    break
            elif scannedSymbol in label:
                foundTransition = True
                break
        if not foundTransition:
            state = TuringMachine.rejectState
        else:
            state = destState
        if foundTransition and writeSymbol:
            if writeSymbol in outSymbols:
                outTape.append(writeSymbol)
            else:
                regTape[regHeadPos] = writeSymbol
        if TuringMachine.isAHaltingState(state):
            stuck = True
            break
        if direction == TuringMachine.leftDir:
            if regHeadPos > 0:
                regHeadPos = regHeadPos - 1
        elif direction == TuringMachine.rightDir:
            regHeadPos = regHeadPos + 1
        
    if verbose: print (regTape, outTape)

    if TuringMachine.isAHaltingState(state):
        return 'stuck, outTape is:' + ''.join(outTape)
    else:
        return 'exceeded maxSteps, outTape is:' + ''.join(outTape)
                    

def testSimulate2TDCM():
    inString = ''
    tmString = rf('unarySequence.tm')
    outString = simulate2TDCM(tmString, inString)
    utils.tprint(outString)
    assert '0010110111011110111110111111011111110111111110' in outString


