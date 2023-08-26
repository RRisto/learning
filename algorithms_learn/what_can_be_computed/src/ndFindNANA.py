# SISO program ndFindNANA.py

# This program searches an input string for any of the four substrings
# 'CACA', 'GAGA', 'TATA', 'AAAA', returning the substring that it
# finds or 'no' if none of the substrings is present. The program
# performs the search in a nondeterministic manner, using a a separate
# thread for each of the four substrings.

# inString: the string to be searched

# returns: if any of the four strings 'CACA', 'GAGA', 'TATA', 'AAAA'
# is found the substring that was found is returned. Otherwise, 'no'
# is returned.
import utils; from utils import rf
from threading import Thread

# function that searches the given input for four different strings, in
# parallel.
def ndFindNANA(inString): 
    # the list of strings to look for
    strings = ['CACA', 'GAGA', 'TATA', 'AAAA'] 

    # create an empty list that will store our threads
    threads = [ ] 

    # create an object that can store a nondeterministic solution
    # computed by other threads
    nonDetSolution = utils.NonDetSolution() 

    # create the threads that will perform the nondeterministic
    # computation
    for string in strings: 
        # create a thread that will execute 
        # findString(string, inString, nonDetSolution) when started
        t = Thread(target=findString, args = (string,inString,nonDetSolution)) 
        # append the newly-created thread to our list of threads
        threads.append(t) 
    
    # Perform the nondeterministic computation. By definition, this
    # means that each thread is started, and we get a return value if
    # either: (a) any thread reports a positive solution, or (b) all
    # threads report negative solutions.
    solution = utils.waitForOnePosOrAllNeg(threads, nonDetSolution) 

    return solution 

# findString is a helper function that sets the nondeterministic solution to 
# the given string if it's found in the given text. This function is intended
# to be executed in a separate thread as part of a nondeterministic
# computation.

# The main body of this program is essentially identical to {\sf \texttt{containsNANA.py}}, 
# but this helper function returns different information.
def findString(string, text, nonDetSolution):  
    if string in text:
        nonDetSolution.setSolution(string) # \textbf{note this difference}   


def testNdFindNANA():
    testVals = [(rf('geneticString.txt'), 'yes'),
                ('T'*100000, 'no'),
                ('T'*100000 + 'TATA', 'yes'),
                ('T'*100000 + 'GAGACCC', 'yes'),
                ('T'*1000 + 'AAAA' + 'C'*1000, 'yes'),
                ]
    for (inString, solution) in testVals:
        val = ndFindNANA(inString)
        prefix = inString[:20]
        utils.tprint(prefix+'...', ':', val)
        if val=='no':
            assert val == solution
        else:
            assert val in ['GAGA', 'CACA', 'AAAA', 'TATA']
            assert val in inString
            
# def testNdFindNANA():
#     for filename in ['geneticString.txt', \
#     ]:
#         inString = rf(filename)
#         result = ndFindNANA(inString)
#         print(filename, ':', result)
#     # kill any lingering threads
# #    utils.killAllThreadsAndExit()

