# SISO program ndContainsNANA.py

# This program searches an input string for any of the four strings
# 'CACA', 'GAGA', 'TATA', 'AAAA', returning 'yes' if any of them is
# found and 'no' otherwise. The program performs the search in a
# nondeterministic manner, using a separate thread for each of the
# four strings.

# inString: the string to be searched

# returns: 'yes' if any of the four strings 'CACA', 'GAGA', 'TATA',
# 'AAAA' is found, and 'no' otherwise.
import utils; from utils import rf
from threading import Thread 

# function that searches the given input for four different strings, in parallel
def ndContainsNANA(inString): 
    # the list of strings to look for
    strings = ['CACA', 'GAGA', 'TATA', 'AAAA'] 

    # create an empty list that will store our threads
    threads = [ ] 

    # create an object that can store a nondeterministic solution computed by
    # other threads
    ndSoln = utils.NonDetSolution() 

    # create the threads that will perform the nondeterministic computation
    for s in strings: 
        # create a thread that will execute findString(s, inString, ndSoln)
        # when started; findString is a helper function defined below
        t = Thread(target=findString,    
                           args = (s, inString, ndSoln)) 
        # append the newly created thread to our list of threads
        threads.append(t) 
    
    # Perform the nondeterministic computation. By definition, this means
    # that each thread is started, and we get a return value if either (a)
    # any thread reports a positive solution, or (b) all threads report
    # negative solutions.
    solution = utils.waitForOnePosOrAllNeg(threads, ndSoln) 

    return solution 

# findString is a helper function that sets the nondeterministic solution to the
# value ``yes'' if the given string is found in the given text. This function is
# intended to be executed in a separate thread as part of a nondeterministic
# computation.
def findString(string, text, ndSoln):  
    if string in text: 
        ndSoln.setSolution('yes') 


def testNdContainsNANA():
    testVals = [(rf('geneticString.txt'), 'yes'),
                ('T'*100000, 'no'),
                ]
    for (inString, solution) in testVals:
        val = ndContainsNANA(inString)
        prefix = inString[:20]
        utils.tprint(prefix+'...', ':', val)
        assert val == solution

