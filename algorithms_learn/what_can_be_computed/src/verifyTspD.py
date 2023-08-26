# SISO program verifyTspD.py

# Verifies a solution to the computational problem TspD.

# The parameters I, S, H are the instance, proposed solution, and hint
# for a verifier as described in Chapter 12.

# The return value is as described in Chapter 12 for verifiers:
# 'correct' if S was successfully verified, and 'unsure' otherwise.
import utils; from utils import rf
from graph import Graph, Path
def verifyTspD(I, S, H): 
    if S == 'no': return 'unsure' 
    # extract G,L from I, and convert to correct data types etc.
    (G,L) = I.split(';')
    G = Graph(G, directed=False); L = int(L)

    # split the hint string into a list of vertices, which will
    # form a Hamilton cycle of length at most L, if the hint is correct
    cycle = Path.fromString(H)
    
    # verify the hint is a Hamilton cycle, and has length at most L
    if G.isHamiltonCycle(cycle) and \
               G.cycleLength(cycle) <= L:
        return 'correct'
    else:
        return 'unsure' 

def testVerifyTspD():
    G = 'a,b,5 a,c,9 b,d,1 d,c,6'
    S = 'yes'
    for (L, H, solution) in [
            (22, 'a,b,d,c', 'correct'), 
            (21, 'a,b,d,c', 'correct'), 
            (20, 'a,b,d,c', 'unsure'), 
            (23, 'a,b,d', 'unsure'), 
            (23, 'a,b,c,d', 'unsure'), 
    ]:
        I = G + ';' + str(L)
        val = verifyTspD(I, S, H)
        utils.tprint(I, H, ':', val)
        assert val == solution

