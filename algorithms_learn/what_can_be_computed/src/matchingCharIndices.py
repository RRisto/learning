# SISO program matchingCharIndices.py

# This program computes solutions to the computational problem
# MatchingCharIndices.

# inString: A single string consisting of two alphanumeric ASCII words w1, w2
# separated by a space.

# returns: A list of all pairs of indices in the input words that match. More
# precisely, writing $w_m[i]$ for the $i$th character of word $m$, the solution is
# a list of pairs $i, j$ such that $w_1[i] = w_2[j]$. Pairs are separated by space
# characters, and the indices in a pair are written in decimal notation
# separated by a comma. 

# example:
# >>> matchingCharIndices('hello world')
# '2,3 3,3 4,1'
import utils; from utils import rf
def matchingCharIndices(inString): 
    # split the input into a list of 2 words
    (word1, word2) = inString.split(' ') 
    # create an empty list that will store pairs of indices
    pairs = [ ] 
    # append every relevant pair of indices to the pairs list
    for i in range(len(word1)): 
        for j in range(len(word2)):
            if word1[i] == word2[j]: 
                thisPair = str(i) + ',' + str(j) 
                pairs.append(thisPair) 
    # concatenate all the pairs together, separated by space characters
    return ' '.join(pairs) 

def testMatchingCharIndices():
    testVals = [('bat ball', '0,0 1,1'),
                ('hello world', '2,3 3,3 4,1'),
                ('a b', ''),
                ('aaa aaaaa', '0,0 0,1 0,2 0,3 0,4 1,0 1,1 1,2 1,3 1,4 2,0 2,1 2,2 2,3 2,4'),
                ('abcdefgh fghijklmnop', '5,0 6,1 7,2'),
    ]
    for (inString, solution) in testVals:
        val = matchingCharIndices(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

