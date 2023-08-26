# file rule110.py

# This file implements the rule 110 automaton as mentioned in the
# textbook. The comments here are brief. Please use an Internet search
# to discover more background information about the Rule 110
# automaton.

import utils; from utils import rf

# Conceptually, we think of the cells of the automaton being filled
# with zeros and ones, but we will encode these as '-' and 'G'
# respectively, since those characters happen to give a more appealing
# visual appearance when successive results are printed out.
zero = '-'
one = 'G'

# updateRule is a dictionary mapping a triple of cells to the new
# value of the middle cell of that triple in the next timestep.
updateRule = {
    (zero, zero, zero): zero,
    (zero, zero, one): one,
    (zero, one, zero): one,
    (zero, one, one): one,
    (one, zero, zero): zero,
    (one, zero, one): one,
    (one, one, zero): one,
    (one, one, one): zero,
    }

def rule110(tape):
    """Implements a single timestep of the Rule 110 automaton.

    Args:

        tape (str): A string representing the current tape of zeros
            and ones.

    Returns:

        str: The updated contents of the tape after a single
            timestep. The left and right ends of the tape are assumed
            to be padded with zeros.

    """
    
    L = len(tape)
    updatedTape = []
    for i in range(L):
        # The left and right ends of the tape need to be treated
        # separately since they should be padded with a zero.
        if i==0:
            # pad with a zero on the left
            (left, middle, right) = (zero, tape[i], tape[i+1])
        elif i==L-1:
            # pad with a zero on the right
            (left, middle, right) = (tape[i-1], tape[i], zero)
        else:
            # no padding required as we are in the interior of the tape
            (left, middle, right) = (tape[i-1], tape[i], tape[i+1])
        newSymbol = updateRule[ (left, middle, right) ]
        updatedTape.append(newSymbol)
    return ''.join(updatedTape)

def testRule110():
    stringLength = 64
    iterations = 40
    startString = [zero for x in range(stringLength)]
    oneLocations = [stringLength-25, stringLength-1]
    # put a single one at each specified location
    for location in oneLocations:
        startString[location] = one

    tape = startString
    for i in range(iterations):
        utils.tprint(tape)
        tape = rule110(tape)

    expectedTape = 'GGGGGG----G-GGG-GGGG---GGG---G-GGG--GG---G--GG-GGGGGG-----GG---G'
    assert tape == expectedTape

        
