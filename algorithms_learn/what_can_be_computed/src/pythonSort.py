# SISO program pythonSort.py

# Sorts the words in an ASCII string into lexicographical
# order, using Python's built-in sorting algorithm.

# inString: Represents a list of words separated by whitespace.

# returns: A string consisting of the input words sorted into
# lexicographical order and separated by space characters.

# Example:
# >>> pythonSort('cap bat apple')
# 'apple bat cap'
import utils; from utils import rf
def pythonSort(inString): 
    words = sorted(inString.split());
    return ' '.join(words) # single string of words separated by spaces    


def testPythonSort():
    testvals = [('here is no water but only rock', 'but here is no only rock water'),
                ('', ''),
                ('xxxx', 'xxxx'),
                ('apple banana apple', 'apple apple banana'),
    ]

    for (inString, solution) in testvals:
        val = pythonSort(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
