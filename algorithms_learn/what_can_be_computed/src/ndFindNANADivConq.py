# SISO program ndFindNANADivConq.py

# This program searches an input string for any of the four substrings
# 'CACA', 'GAGA', 'TATA', 'AAAA', returning the substring that it
# finds or 'no' if none of the substrings is present. The program
# performs the search in a nondeterministic manner, using a divide and
# conquer approach.

# inString: the string to be searched

# returns: if any of the four strings 'CACA', 'GAGA', 'TATA', 'AAAA'
# is found the substring that was found is returned. Otherwise, 'no'
# is returned.
import utils; from utils import rf
from threading import Thread
import threading

# A list of the desired substrings to search for.
strings = ['CACA', 'GAGA', 'TATA', 'AAAA']
# Maximum length of a desired substring.
maxDesiredStringLen = max([len(x) for x in strings])
# Maximum depth of the computation tree.
maxDepth = 7

        
def ndFindNANADivConq(inString):
    rootNdSoln = utils.NonDetSolution()
    ndFindNANAHelper(inString, rootNdSoln)
    return rootNdSoln.getSolution()

# Deterministic version of findNANA for the base case---will be
# applied at each leaf of the computation tree.
def findNANA(text):
    for string in strings:
        if string in text:
            return string
    return 'no'



def ndFindNANAHelper(text, parentNdSoln, depth=0): 
    if depth == maxDepth:
        # We are at a leaf of the computation tree.
        solution = findNANA(text)
        parentNdSoln.setSolution(solution)
    else:
        # We are at an internal node of the computation tree. Split the
        # given text into two halves, and launch new threads to search
        # each half separately.
        threads = [ ] 
        childNdSoln = utils.NonDetSolution() 
        halfway = int(len(text)/2)
        # We will split the input text in half, but we could get
        # unlucky and find that one of the desired substrings
        # straddles the point of the split. Therefore, extend both
        # halves by the maximum length of a desired substring.
        upperLimit = min(halfway + maxDesiredStringLen, len(text))
        lowerLimit = max(halfway - maxDesiredStringLen, 0)
        text1 = text[:upperLimit]
        text2 = text[lowerLimit:]
        t1 = Thread(target=ndFindNANAHelper, args = (text1,childNdSoln,depth+1))
        t2 = Thread(target=ndFindNANAHelper, args = (text2,childNdSoln,depth+1))
        threads.append(t1)
        threads.append(t2)
        solution = utils.waitForOnePosOrAllNeg(threads, childNdSoln)
        parentNdSoln.setSolution(solution)


def testNdFindNANADivConq():
    testVals = [
        ('1000Ts', 1000*'T', 'no'),
        ('1000Ts1GAGA', 1000*'T'+'GAGA', 'yes'),
        ('1millionTs', 1000000*'T', 'no'),
        ('1millionTs1GAGA', 1000000*'T'+'GAGA', 'yes'),
        ('10millionTs', 10000000*'T', 'no'),
        ('10millionTs1GAGA', 10000000*'T'+'GAGA', 'yes'),
        ('10000CACAs10000TATAs', 10000*'CACA'+10000*'TATA', 'yes'),
        ('10000CACAs10000TATAs', 10000*'CACA'+10000*'TATA', 'yes'),
        ('10000CACAs10000TATAs', 10000*'CACA'+10000*'TATA', 'yes'),
        ('10000CACAs10000TATAs', 10000*'CACA'+10000*'TATA', 'yes'),
        ('10000CACAs10000TATAs', 10000*'CACA'+10000*'TATA', 'yes'),
        ]
    for (desc, inString, solution) in testVals:
        val = ndFindNANADivConq(inString)
        utils.tprint(desc, ':', val)
        if val=='no':
            assert val == solution
        else:
            assert val in ['GAGA', 'CACA', 'AAAA', 'TATA']
            assert val in inString
        utils.NonDetSolution.printLock.acquire()
        utils.tprint(desc, ':', val)
        utils.NonDetSolution.printLock.release()

