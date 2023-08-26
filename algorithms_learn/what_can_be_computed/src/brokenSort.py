# SISO program brokenSort.py

# This is a deliberately broken implementation of a sorting algorithm
# for sorting the words in an ASCII string into lexicographical
# order. The implementation works correctly when all words in the
# input are unique, but enters an infinite loop if there are
# duplicates in the input.

# inString: Represents a list of words separated by whitespace.

# returns: If there are no duplicate words in the input, a string
# consisting of the input words sorted into lexicographical order and
# separated by space characters is returned. If there are duplicates,
# the function enters an infinite loop.

# Example:
# >>> brokenSort('cap bat apple')
# 'apple bat cap'
import utils; from utils import rf
def brokenSort(inString):  
    words = inString.split();
    while not isSorted(words): 
        for i in range(len(words)-1):
            if words[i+1] < words[i]:
                # swap elements i and i+1
                words[i], words[i+1] = words[i+1], words[i]
    return ' '.join(words) # single string of words separated by spaces

def isSorted(words):
    for i in range(len(words)-1):
        # next line is a BUG: should be \str{<}, not \str{<=}
        if words[i+1] <= words[i]:    
            return False
    return True 
        
def testBrokenSort():
    testvals = [('here is no water but only rock', 'but here is no only rock water'),
                ('', ''),
                ('xxxx', 'xxxx'),
                ('apple banana apple', None), # brokenSort enters infinite loop for duplicate values
    ]

    for (inString, solution) in testvals:
        val = utils.runWithTimeout(None, brokenSort, inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
