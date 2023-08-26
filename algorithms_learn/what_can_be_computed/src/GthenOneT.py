# SISO program GthenOneT.py

# Returns 'yes' if the input string is a member of the language
# GthenOneT, and 'no' otherwise. The language GthenOneT consists of
# strings s with the following property: there is at least one G
# character (say at index n) such that s contains exactly one T
# character after n or exactly one T character before n. The purpose
# of this rather strange language is to demonstrate the use of
# nondeterminism. Although it would be relatively easy to write a
# deterministic program to determine membership of the GthenOneT
# language, the program below uses a nondeterministic
# approach. Specifically, it nondeterministically searches all
# possible strings to the left and right of a ``G'', returning ``yes''
# if any of those strings contain exactly one ``T''.

# Example:
# >>> GthenOneT('GTTCCCGTGAATCCCC')
# 'yes'
import utils; from utils import rf
from threading import Thread

def GthenOneT(inString):
    threads = [ ]
    ndSoln = utils.NonDetSolution()
    for i in range(0, len(inString)):
        if inString[i] == 'G':
            leftString = inString[:i]
            leftThread = Thread(target=findT, args = (leftString, ndSoln))
            threads.append(leftThread)
            rightString = inString[i+1:]
            rightThread = Thread(target=findT, args = (rightString, ndSoln))
            threads.append(rightThread)
    return utils.waitForOnePosOrAllNeg(threads, ndSoln)

# findT is a helper function that sets solution to ``yes'' if there is
# exactly one ``T'' in the given searchString.
def findT(searchString, nonDetSolution):
    if searchString.count('T')==1:
        nonDetSolution.setSolution('yes')

def testGthenOneT():
    testvals = [('xx', 'no'),
                ('xTx', 'no'),
                ('xCGTTTGAATATx', 'no'),
                ('xCGGAAGGAx', 'no'),
                ('xTGx', 'yes'),
                ('xTGTx', 'yes'),
                ('xTTGTGTTGTTGAACCTAAx', 'yes')]
    for (inString, solution) in testvals:
        val = GthenOneT(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

