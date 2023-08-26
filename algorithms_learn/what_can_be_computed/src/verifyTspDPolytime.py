# SISO program verifyTspDPolytime.py

# Verifies a solution to the computational problem TspD, in
# polynomial time.

# The parameters I, S, H are the instance, proposed solution, and hint
# for a verifier as described in Chapter 12.

# The return value is as described in Chapter 12 for verifiers:
# 'correct' if S was successfully verified, and 'unsure' otherwise.
import utils; from utils import rf
from graph import Graph, Path
def verifyTspDPolytime(I, S, H): 
    # reject excessively long solutions and hints
    if len(S) > len(I) or len(H) > len(I):  
        return 'unsure'
    # The remainder of the program is identical to verifyTspD.py
    # ...
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

def testVerifyTspDPolytime():
    G = 'a,b,5 a,c,9 b,d,1 d,c,6'
    for (L, S, H, solution) in [
            (22, 'yes', 'a,b,d,c', 'correct'), 
            (21, 'yes', 'a,b,d,c', 'correct'), 
            (20, 'yes', 'a,b,d,c', 'unsure'), 
            (23, 'yes', 'a,b,d', 'unsure'), 
            (23, 'yes', 'a,b,c,d', 'unsure'), 
            (23, 'yes', 'a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a', 'unsure'), 
            (23, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'a,b,c,d', 'unsure'), 
    ]:
        I = G + ';' + str(L)
        val = verifyTspDPolytime(I, S, H)
        utils.tprint(I, S, H, ':', val)
        assert val == solution

