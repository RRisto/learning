# SISO program haltExTuring.py

# Solves the computational problem haltEx, for the case of input
# programs represented as Turing machines.

# progString: An ASCII description of a Turing machine M

# inString: The initial content I of the Turing machine's tape

# returns: If the computation of M(I) halts in fewer than $2^{len(I)}$
# steps, return 'yes' and otherwise return 'no'.

# Example:
# >>> haltExTuring(rf('containsGAGA.tm'), 'TTTTTTTT')
# 'yes'
import utils; from utils import rf
# We import the TuringMachine class for fine-grained  
# control of Turing machine simulation.
from turingMachine import TuringMachine 
def haltExTuring(progString, inString):
    # construct the Turing machine simulator
    sim = TuringMachine(progString, inString) 
    # simulate for at most $2^n-1$ steps
    for i in range(2**len(inString)-1): 
        sim.step() 
        if sim.halted: 
            return 'yes'
    return 'no'  

def testHaltExTuring():
    rf = utils.rf
    progString = rf('containsGAGA.tm')
    inStrings = [i*'G' for i in range(10)]
    for inString in inStrings:
        solution = haltExTuring(progString, inString)
        utils.tprint(inString, solution)
        sim = TuringMachine(progString, inString)
        sim.run()
        if sim.steps < 2**len(inString):
            val = 'yes'
        else:
            val = 'no'
        assert val == solution

