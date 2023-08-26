# SISO program bubbleSort.py

# Sorts the words in an ASCII string into lexicographical
# order, using the well-known bubble sort algorithm.

# inString: Represents a list of words separated by whitespace.

# returns: A string consisting of the input words sorted into
# lexicographical order and separated by space characters.

# Example:
# >>> bubbleSort('cap bat apple')
# 'apple bat cap'
import utils; from utils import rf
def bubbleSort(inString):  
    words = inString.split();
    while not isSorted(words):
        for i in range(len(words)-1):
            if words[i+1] < words[i]:
                # swap elements i and i+1
                words[i], words[i+1] = words[i+1], words[i]
    return ' '.join(words) # single string of words separated by spaces 

def isSorted(words):
    for i in range(len(words)-1):
        if words[i+1] < words[i]:
            return False
    return True        
        
def testBubbleSort():
    testvals = [('here is no water but only rock', 'but here is no only rock water'),
                ('', ''),
                ('xxxx', 'xxxx'),
                ('apple banana apple', 'apple apple banana'),
    ]

    for (inString, solution) in testvals:
        val = bubbleSort(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
