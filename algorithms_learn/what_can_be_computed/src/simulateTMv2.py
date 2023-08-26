# SISO program simulateTMv2.py

# Simulate a given Turing machine with a given input.  simulateTMv2 is
# provided as a self-contained implementation of a Turing machine
# simulator using only elementary Python.  Note that the book
# materials also provide a more sophisticated and robust Turing
# machine simulator called simulateTM.py. However, that simulator uses
# object-oriented Python, which requires additional effort to
# understand. Also note that simulateTMv2 is not quite a genuine SISO
# program because we allow an optional boolean parameter, but this can
# be ignored.

# tmString: ASCII description of the machine M to be simulated

# inString: the initial content I of M's tape

# verbose: optional boolean indicating whether extra output should be printed

# returns: the tape content when M enters a halting state

# Example:
# >>> simulateTMv2(rf('binaryIncrementer.tm'), 'x100111x')
# 'x101000x'



import utils; from utils import rf
import re
def simulateTMv2(tmString, inString, verbose = False):
    # key is state, value is list of transitions
    transitions = dict()
    tmLines = [x.strip() for x in tmString.split('\n')]
    for line in tmLines:
        if len(line)>0:
##            print('line:','**'+line+'**')
            (states, label, actions) = [x.strip() for x in re.split('[:;]',line)]
            (sourceState, destState) = [x.strip() for x in states.split('->')]
##            print('splitline:',(sourceState, destState, label, actions))
            if ',' in actions:
                (writeSymbol, direction) = actions.split(',')
            else:
                (writeSymbol, direction) = (None, actions)
##            print('splitline:',(sourceState, destState, label, writeSymbol, direction))
            transitionList = transitions.setdefault(sourceState, [])
            transitionList.append( (destState, label, writeSymbol, direction) )

##    print (transitions)

    tape = [c for c in inString]
    state = 'q0'
    headPos = 0
    halted = False
    steps = 0
    maxSteps = 1000

    while not halted and steps < maxSteps:
        steps = steps + 1
        if verbose: print(steps, tape, headPos)
        if headPos == len(tape):
            # underscore character will represent a blank
            tape.append('_')
        scannedSymbol = tape[headPos]
        transitionList = transitions[state]
        foundTransition = False
        for (destState, label, writeSymbol, direction) in transitionList:
            if '~' == label:
                foundTransition = True
                break
            elif label[0] == '!':
                if scannedSymbol not in label[1:]: 
                    foundTransition = True
                    break
            elif scannedSymbol in label:
                foundTransition = True
                break
        if not foundTransition:
            state = 'qR'
        else:
            state = destState
        if foundTransition and writeSymbol:
            tape[headPos] = writeSymbol
        if state == 'qA' or state == 'qR' or state == 'qH':
            halted = True
            break
        if direction == 'L':
            if headPos > 0:
                headPos = headPos - 1
        elif direction == 'R':
            headPos = headPos + 1
            
        
    if verbose: print (tape)

    if state == 'qA':
        return 'yes'
    elif state == 'qR':
        return 'no'
    elif state == 'qH':
        return ''.join(tape)
    else:
        return 'exceeded maxSteps'
                    

def testSimulateTMv2():
    for (filename, inString, solution) in [
            ('containsGAGA.tm', 'CCCCCCCCCAAAAAA', 'no'),
            ('containsGAGA.tm', 'CCCGAGACCAAAAAA', 'yes'),
            ('binaryIncrementer.tm', 'x100111x', 'x101000x'),
            ]:
        val = simulateTMv2(rf(filename), inString)
        utils.tprint('filename:', filename, 'inString:', inString, 'result:', val)
        assert val == solution

