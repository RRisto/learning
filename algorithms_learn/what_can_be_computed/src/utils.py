"""Utilities module for the textbook "What Can Be Computed?" (WCBC)

This "utils" module provides various supporting functions for use with
the programs provided is online materials for the textbook "What Can
Be Computed?" (WCBC). (For an overview of the entire collection of
programs, see the file README.txt in this directory.) 

Functionality provided by the utils module includes: reading and
writing text files, extracting names of functions from Python files
(useful for universal computation simulations), encoding multiple
strings as single strings and vice versa, creating random strings of
various kinds, manipulating alphabets such as the ASCII alphabet,
executing code with a timeout (in case it runs for a long time or
forever), formatting sets of strings, manipulating solutions of
nondeterministic programs, an exception class specific to WCBC,
facilities for testing.
"""

# The following line improves compatibility with Python version 2.x
from __future__ import print_function

# Check that the version of Python being used is sufficiently recent.
import sys
def checkPythonVersion(shouldExit = True):
    """Check that the version of Python is recent enough (>=2.7).

    If the version is too old, exit Python immediately unless instructed otherwise.

    Args:
    
        shouldExit (bool): Indicates the action that should be taken
            if the version of Python is too old. If True, exit
            immediately. Otherwise, print a warning message but then
            return.
    """
    if sys.version_info < (2, 7):
        print("Sorry, but there's a problem: you need Python version at least 2.7. Exiting now.")
        if shouldExit:
            sys.exit()

checkPythonVersion()

# Import all the modules we need.
import re, sys, threading, random, time, os, os.path

# Importing the queue module is a little tricky, since the name was
# changed in version 3. The following code takes care of this issue.
if sys.version_info < (3, 0):
    import Queue
    queue = Queue
else:
    import queue

haltComputations = threading.Event()
"""An event that signals long-running computations to exit."""

aRandom = random.Random()
"""A random number generator that can be used by all functions that
want one.
"""

inf = float('inf')
"""A value representing positive infinity.

In version >= 3.5 of Python, math.inf would be more elegant here, but
it's better to use an idiom that also works with earlier versions of
Python.

"""

def extractMainFunctionName(progString):
    """Extract the name of the main function in a Python program.

    Given a Python program as defined in the book, return a string
    containing the name of the "main" function: that is, the first
    Python function defined within progString. This is done by
    searching for the first line that begins with the characters "def"
    followed by whitespace, then returning the identifier immediately
    following that whitespace. Clearly, this is not infallible, but it
    works for all of the example programs provided with the book
    materials. If desired, one could use Python parsing tools to
    locate the first defined function with perfect reliability. But
    that approach is more complex than we need for the illustrative
    examples provided with the book.

    Args:
    
        progString (str): string containing the Python program to be
        examined.

    Returns: 

        str: The name of the main function if one could be found,
           otherwise the empty string.

    """
    
    # This is the regular expression that searches for the main
    # function using the heuristic described above.
    mainFunctionRegex = r'^def\s+([a-zA-Z0-9_]*)'
    matchResult = re.search(mainFunctionRegex, progString, re.MULTILINE )
    if matchResult:
        return matchResult.group(1)
    else:
        # Return empty string if we couldn't find any function
        # definitions. This should never happen when processing a
        # legitimate SISO program.
        return ''

def extractMainFunction(progString, localVars):
    """Given a Python program as defined in the book, return a reference
    to the "main" function: that is, the first Python function defined
    within progString. The localVars parameter should be 

    Args:
    
        progString (str): string containing the Python program to be
            examined.

        localVars (dict): the "locals()" dictionary of the calling
            function, as explained further in the source code comment.

    Returns: 

        fn: A reference to the main function if one could be
            found. Otherwise a WcbcException is raised.

    """

    functionName = extractMainFunctionName(progString)
    # Python has a standard built-in dictionary called "locals()"
    # which contains, among other things, all the functions that are
    # currently defined. We can get a reference to the desired
    # function by looking it up in this dictionary, using the name of
    # the function as the key.
    if functionName in localVars:
        progFunction = localVars[functionName]
    else:
        raise WcbcException('function ' + functionName + \
                            ' not defined, so cannot extract or simulate it')
    return progFunction


def readFile(fileName):
    """Read a file, returning its contents as a single string.

    Args:
    
        fileName (str): The name of the file to be read.

    Returns: 

        str: The contents of the file.
    """

    fileContents = ''
    with open(fileName) as inputFile:
        fileContents = inputFile.read()
    return fileContents

# Define a very short convenient alias for the readFile function
rf = readFile


def writeFile(fileName, fileContents):
    """Write a file, overwriting any existing content with the given content.

    Args:
    
        fileName (str): The name of the file to be written or overwritten.

        fileContents (str): The contents of the file to be written,
            stored as a single string that may contain newlines.
    """
    with open(fileName, 'w') as outputFile:
        outputFile.write(fileContents)


def ESS(inString1, inString2):
    """Encode two strings as a single string.

    ESS is an acronym for Encode as Single String.  This function uses
    the encoding method suggested in the textbook: the encoding
    consists of the length of the first string, followed by a space
    character, followed by the two strings concatenated together.

    Args:
    
        inString1 (str): The first string to be encoded

        inString2 (str): The second string to be encoded

    Returns: 

        str: A single string encoding inString1 and inString2

    Example:
        
        >>> ESS('abc', 'defg')
        '3 abcdefg'
    """
    return str(len(inString1)) + ' ' + inString1 + inString2

def DESS(inString):
    """Decode a single string into two strings (inverse of ESS).

    DESS is an acronym for DEcode from Single String. This function
    uses the method suggested in the textbook for converting a single
    string that encodes two strings back into the original two
    strings. DESS is the inverse of the function ESS.

    Args:
    
        inString (str): The string to be decoded

    Returns: 

        (str, str): A 2-tuple containing the two strings that were decoded from the input.

    Example:
        
        >>> DESS('3 abcdefg')
        ('abc', 'defg')
        
    """
    # split on the first space character
    (theLength, remainder) = inString.split(' ', 1)
    inString1 = remainder[:int(theLength)]
    inString2 = remainder[int(theLength):]
    return (inString1, inString2)


def randomAlphanumericString(length = None, maxLength = 20):
    """Generate a random alphanumeric string.

    This function generates and returns a random alphanumeric string,
    where the length of the string can be specified or can also be
    selected randomly. The individual characters in the string are
    selected uniformly at random.

    Args:
    
        length (int): The desired length of the string. Defaults to
           None. If None, the length of the string will be chosen
           uniformly at random between 0 and maxLength-1.

        maxLength: When the length of the string is chosen at random,
           the maximum length is maxLength-1. This parameter is only
           relevant if length is None.

    Returns: 

        str: The randomly generated alphanumeric string.

    """
    
    characters = 'abcdefghijklmnopqstuvwxyzABCDEFGHIJKLMNOPQSTUVWXYZ0123456789'
    if length == None:
        length = aRandom.randint(0,maxLength)
    chosenCharacters = []
    for i in range(length):
        randomCharacter = aRandom.choice(characters)
        chosenCharacters.append(randomCharacter)
    return ''.join(chosenCharacters)



def randomDigitalString(length = None, maxLength = 20):
    """Generate a random string of numeric digits.

    This function generates and returns a random string of numeric
    digits, where the length of the string can be specified or can
    also be selected randomly. The individual digits in the string are
    selected uniformly at random, except that the first digit cannot
    be 0.

    Args:
    
        length (int): The desired length of the string. Defaults to
           None. If None, the length of the string will be chosen
           uniformly at random between 0 and maxLength-1.

        maxLength: When the length of the string is chosen at random,
           the maximum length is maxLength-1. This parameter is only
           relevant if length is None.

    Returns: 

        str: The randomly generated string of digits.

    """

    characters = '0123456789'
    if length == None:
        length = aRandom.randint(0,maxLength)
    chosenCharacters = []
    for i in range(length):
        randomCharacter = aRandom.choice(characters)
        # first character must be nonzero
        while i==0 and randomCharacter=='0':
            randomCharacter = aRandom.choice(characters)
        chosenCharacters.append(randomCharacter)
    return ''.join(chosenCharacters)

def randomString(alphabet, length = None, maxLength = 20):
    """Generate a random string of characters from a given up a bit.

    This function generates and returns a random string of characters
    from a given alphabet, where the length of the string can be
    specified or can also be selected randomly. The individual
    characters in the string are selected uniformly at random.

    Args:

        alphabet (list of characters): A list of characters in the
            alphabet to be used.
    
        length (int): The desired length of the string. Defaults to
           None. If None, the length of the string will be chosen
           uniformly at random between 0 and maxLength-1.

        maxLength: When the length of the string is chosen at random,
           the maximum length is maxLength-1. This parameter is only
           relevant if length is None.

    Returns: 

        str: The randomly generated string.

    """

    characters = alphabet
    if length == None:
        length = aRandom.randint(0,maxLength)
    chosenCharacters = []
    for i in range(length):
        randomCharacter = aRandom.choice(characters)
        chosenCharacters.append(randomCharacter)
    return ''.join(chosenCharacters)


def asciiAlphabetAsList():
    """Return a list consisting of the 128 ASCII characters"""
    
    asciiAlphabet = []
    for i in range(128):
        asciiAlphabet.append(chr(i))
    return asciiAlphabet

ASCII_ALPHABET = asciiAlphabetAsList()
"""A list consisting of the 128 ASCII characters"""

def geneticAlphabetAsList():
    """Return a list consisting of the 4 characters 'A', 'C', 'G', 'T'"""
    return ['A', 'C', 'G', 'T']


def boolToYes(b):
    """Convert a Boolean input into 'yes' or 'no'

    Args:

        b (bool): The Boolean value to be converted
    
    Returns: 

        str: 'yes' if b is True, and 'no' otherwise.

    """
    if b:
        return 'yes'
    else:
        return 'no'

def nextShortLex(s, alphabet):
    """Return the next string in shortlex ordering on a given alphabet.

    Shortlex is an ordering that lists strings according to length,
    with strings of the same length being ordered
    lexicographically. This function takes a string on some particular
    alphabet as input, and returns the next string on that alphabet in
    the shortlex ordering.

    Args:

        s (str): The string whose successor will be returned.

        alphabet (list of characters): A list of characters in the
            alphabet to be used.
    
    Returns: 

        str: The successor of s in the shortlex ordering, assuming the
            given alphabet.

    Example:
        
        >>> nextShortLex('aab', ['a', 'b', 'c'])
        'aac'
        >>> nextShortLex('ccc', ['a', 'b', 'c'])
        'aaaa'
    """

    first = alphabet[0]
    last = alphabet[-1]
    if s=='': return str(first)
    chars = [c for c in s]
    L = len(chars)
    # The Boolean variable overflow will indicate whether or not this
    # is the last string of the current length (and hence whether we
    # need to "overflow" to the first string with length one greater)
    overflow = True
    for i in range(L-1,-1,-1):
        currentChar = chars[i]
        if currentChar != last:
            overflow = False
            break
    # Either we overflowed (and i=0), or we didn't overflow, in which
    # case the value of i is now the index of the rightmost character
    # that can be incremented. Let's remember all the needed
    # information about that character.
    incrementIndex = i
    incrementChar = currentChar
    alphabetIndex = alphabet.index(currentChar)
    
    if overflow:
        # Treat overflow as a special case and return a string of
        # length L+1 consisting entirely of the first character in the
        # alphabet.
        return first*(L+1)
    else:
        # We didn't overflow, so manipulate the array of characters to
        # produce the next string in lexicographic order. The
        # rightmost character that can be incremented gets
        # incremented...
        chars[incrementIndex] = alphabet[alphabetIndex+1]
        # ...then all the characters to the right of that roll over to
        # the first character in the alphabet.
        for j in range(incrementIndex+1,L):
            chars[j]=first
        return ''.join(chars)



def nextASCII(s):
    """Return the successor of ASCII string s in the shortlex ordering.

    For a detailed explanation, see the documentation of
    nextShortLex(). This function is the same as nextShortLex(), for
    the special case where the alphabet is the ASCII alphabet.

    Args:

        s (str): The ASCII string whose successor will be returned.

    Returns: 

        str: The successor of ASCII string s in the shortlex ordering.

    """
    return nextShortLex(s, ASCII_ALPHABET)


# Enter supposedly infinite loop.  In fact, we exit if the event
# haltComputations is signalled, or if the fixed timeout expires.
# This helps to prevent problems with automated testing of code that
# enters infinite loops.
def loop():
    """Enter an infinite loop, but with features that facilitate testing.

    This function supposedly enters an infinite loop. The intention is
    that it should be used for simulating infinite loops, but in fact
    it is more sophisticated. The function waits on the
    utils.haltComputations event, and exits immediately if that event
    is signaled. This facilitates testing of code that deliberately
    enters infinite loops. In addition, this function times out after
    60 seconds. This prevents background threads looping indefinitely.

    """
 
    timeout = 60 # one minute should be plenty
    haltComputations.wait(timeout)
    # reset the haltComputations event
    haltComputations.clear()


def invokeAndStoreResult(fn, q, done, *inStrings):
    """Invoke a function and store its return value in a given queue.

    Mostly intended as a private function used by
    utils.runWithTimeout(). The invokeAndStoreResult() function
    invokes a function (which itself is passed in as a parameter) with
    certain arguments (also passed in as parameters), stores the
    result in a queue data structure, then signals an event to declare
    that it is finished. This makes it possible for other threads to
    be aware of when the function has completed and for those threads
    to obtain its return value.

    Args:

        fn (a function): The function that will be invoked.

        q (a Python queue.Queue): A queue that will be used for storing the
            return value. A queue is used because Python queues happen
            to behave well in multithreaded environments. In fact, at
            most one item will be stored in this queue.

        done (a Python threading.Event): An event that will be
            signaled when fn has returned.

        *inStrings: A variable number of arguments that will be passed
            on to fn.

    """
    ret = fn(*inStrings)
    q.put(ret)
    done.set()
        
def runWithTimeout(timeout, fn, *inStrings):
    """Invoke a function with a timeout.

    This invokes a function (which itself is passed in as a parameter)
    with certain arguments (also passed in as parameters). If the
    function completes within the given timeout, its return value is
    returned. Otherwise, None is returned.

    Args:

        timeout (float): The number of seconds before the function
            invocation times out. If None, this is set to a standard
            value for running unit tests.

        fn (a function): The function that will be invoked.

        *inStrings: A variable number of arguments that will be passed
            on to fn.

    Returns: 

        object: None if fn times out, otherwise the return value of fn.

    """
    
    if timeout == None:
        timeout = TEST_TIMEOUT

    # a queue for storing the return value of fn   
    q = queue.Queue()
    # an event for signaling when fn has completed
    done = threading.Event()

    # create and start a separate thread in which to invoke the
    # function
    t = threading.Thread(target=invokeAndStoreResult, args=(fn, q, done) + inStrings)
    t.start()

    # wait for either the function to complete, or the duration of the
    # timeout, whichever is earlier
    done.wait(timeout)

    # If it's a long-running computation that knows about the
    # haltComputations event, tell it to stop now.
    haltComputations.set()

    # Reset for future computations
    haltComputations.clear()

    # if the queue is empty, the function did not complete, so return
    # None
    if q.empty():
        retVal = None
    else:
        retVal = q.get()

    return retVal

    

def formatASet(theSet):
    """Format a set of strings as a string.

    The given set is returned enclosed by braces and with elements
    separated by commas.

    Args:

        theSet (set of str): The set to be formatted.

    Returns: 

        str: A string representing theSet, enclosed by braces and with
             elements separated by commas.

    Example:
        >>> formatASet({'abc', 'd', 'ef'})
        '{d,ef,abc}'
    
    """
    return '{' + ','.join(theSet) + '}'

def formatSetOfSets(theSets):
    """Format a set of frozensets of strings as a single string.

    Each frozenset of strings is formatted using utils.formatASet(),
    and the resulting strings are separated by space characters.

    Args:

        theSets (set of frozensets of str): The set of frozensets to
            be formatted.

    Returns: 

        str: A string representing theSets.

    Example:
        >>> set1 = frozenset({'abc', 'd', 'ef'})
        >>> set2 = frozenset({'w', 'xy', 'z'})
        >>> formatSetOfSets({set1, set2})
        '{ef,abc,d} {xy,z,w}'

    """
    formattedSets = [formatASet(s) for s in theSets]
    return ' '.join(formattedSets)


def sortByNthElement(theList, N):
    """Sort a list of items by the Nth element of each item.

    Args:

        theList (iterable of indexable items): The list of items to be sorted.

        N (int): The index of the elements that should be used for the sorting.

    Returns: 

        list: A new list sorted in increasing order by the Nth element of each item in theList.
    
    """
    return sorted(theList, key=lambda x: x[N])

def killAllThreadsAndExit():
    """Exit Python, which also kills all Python threads.

    This is useful for debugging and in certain other situations,
    since there is no reliable way to kill Python threads.

    """

    # Best to flush any messages before we exit, otherwise they may
    # not be printed.
    sys.stdout.flush()
    os._exit(0)

class NonDetSolution:
    """Manages solutions to nondeterministic programs.

    NonDetSolution is a class that can be used to arrange for
    nondeterministic (i.e. multithreaded) Python programs to return a
    value. For an example of how to use it, see the program
    ndContainsNANA.py, which is also explained in the book. The basic
    idea is to create a single NonDetSolution object nds to be used by
    the nondeterministic program. The nds object will be passed to
    each thread created, then nds and the list of threads will be
    passed to waitForOnePosOrAllNeg() in order to obtain the program's
    solution.

    """

    
    printLock = threading.Lock()
    """A static lock shared between all NonDetSolution objects -- the
    intention is that this can be used for debugging. Specifically,
    you can acquire the printLock, print some debugging information,
    then release the lock.

    """
    
    def __init__(self):
        self.solution = 'no'
        """str: Stores the solution to the problem being solved. By default,
        it has the value 'no'."""
        
        # This lock protects access to the above solution field.
        self.solnLock = threading.Lock()
        """threading.Lock: protects access to the above solution field"""
        
        self.done = threading.Event()
        """threading.Event: Will be used to signal when either a positive
        solution has been found or all threads have terminated with
        negative solutions."""


    def waitUntilDone(self):
        """Wait until we receive the signal that a positive solution has been
        found or all threads have terminated negatively."""
        self.done.wait()

    def setDone(self):
        """Send the signal that a positive solution has been found or all
        threads have terminated negatively."""
        self.done.set()

    def setSolution(self, solution):
        """Set the solution to the given value, and signal if it's positive.

        This is a setter for the solution attribute. In addition, if
        the new value for the solution attribute is positive
        (i.e. anything other than the string "no"), we signal this
        object's event attribute, done. This will enable other threads
        to become aware that a positive solution has been found.

        """
        
        # We only take action for positive solutions. If the given
        # solution is 'no', we leave the default value of 'no'
        # untouched -- and if another thread has meanwhile set the
        # solution to a positive value, we should certainly not set it
        # back to 'no' because positive solutions take precedence
        # anyway.
        if solution != 'no':
            self.solnLock.acquire()
            self.solution = solution
            self.solnLock.release()
            # Signal that a positive solution has been found.
            self.setDone()

    def getSolution(self):
        """Return the stored value of the solution."""
        self.solnLock.acquire()
        solution = self.solution
        self.solnLock.release()
        return solution

def waitForOnePosOrAllNeg(threads, nonDetSolution):
    """Wait until one of the threads terminates positively or all terminate negatively.

    Each of the threads in the given list will be started. Each of
    these threads must already possess a reference to the given
    nonDetSolution instance, since this will be used to signal if and
    when a positive solution is found. When a positive solution is
    found by one of the threads, the value of that solution is
    returned. Otherwise, we wait until threads terminate and then
    return the negative solution, 'no'.

    Args:
        threads (list of threading.Thread): Threads that will be started.

        nonDetSolution (NonDetSolution): A NonDetSolution object used
        to store and manipulate the solution being computed by the
        given threads.

    Returns:
        str: The solution that was found.

    """

    # check to see if the number of threads is getting too big
    maxThreads = 500
    if len(threads) + threading.active_count() > maxThreads:
        NonDetSolution.printLock.acquire()
        print('Fatal error in waitForOnePosOrAllNeg: you attempted to run more than', 
              maxThreads,
              '''threads simultaneously.  
In theory this isn't a problem, but in practice your Python
implementation may encounter difficulties. To avoid these potential
problems, all threads will now be killed.''')
        NonDetSolution.printLock.release()
        killAllThreadsAndExit()
    
    
    # start each thread
    for t in threads:
        # print('starting', t)
        t.start()

    # create and start yet another thread, whose job it will be to
    # detect when all the other threads have terminated
    allTerminatedThread = threading.Thread(target=waitAllTerminated, \
                                     args = (threads, nonDetSolution))
    allTerminatedThread.start()
    nonDetSolution.waitUntilDone()
    return nonDetSolution.getSolution()
    

def waitAllTerminated(threads, nonDetSolution):
    """Wait until all the given threads have terminated, then signal. 

    When all threads have terminated, signal this fact via the
    nonDetSolution object.

    Args:
        threads (list of threading.Thread): Threads that will be waited for.

        nonDetSolution (NonDetSolution): A NonDetSolution object used
        to store and manipulate the solution being computed by the
        given threads.

    """

    # wait for each thread to complete
    for t in threads:
        t.join()
    nonDetSolution.setDone()
    


class WcbcException(Exception):
    """A simple wrapper of the standard Python Exception class.

    WcbcException instances are used to indicate unexpected or
    unhandled situations within the WCBC package.

    """
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)



################################################################################
#### The following settings control testing and are not relevant for
#### running "normal" programs that aren't tests.
################################################################################
VERBOSE_TESTS = True
BRIEF_TESTS = True
NUM_BRIEF_TESTS = 1
TEST_TIMEOUT = 10.0
################################################################################

# tprint stands for "test print" -- for printing output in a test function
def tprint(*args, **kwargs):
    """Print output within a test function

    "tprint" stands for "test print". This is a wrapper for the
    standard Python print function. It prints nothing unless
    VERBOSE_TESTS is True.

    """
    
    if VERBOSE_TESTS:
        print(*args, **kwargs)
        sys.stdout.flush()

def isPrime(M):
    """Return True if integer M is prime, and False otherwise.

    This is used for testing certain functions; see e.g. factor.py. A
    simple, inefficient algorithm is employed.

    """
    for x in range(2,M):
        if M%x==0: return False
    return True
