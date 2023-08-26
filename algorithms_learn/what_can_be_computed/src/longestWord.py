# SISO program longestWord.py

# Returns the longest word in the input string. Here, a "word" is
# sequence of characters surrounded by whitespace.
import utils; from utils import rf
def longestWord(inString): 
    words = inString.split()
    longest = ''
    lengthOfLongest = 0
    for word in words:
        if len(word) > lengthOfLongest:
            longest = word
            lengthOfLongest = len(word)
    return longest 

def testlongestWord():
    testVals = [('', ''),
                ('a', 'a'),
                ('abc', 'abc'),
                ('a bc', 'bc'),
                ('bc a', 'bc'),
                ('x xx xxx xxxx xxxxx xxxx xxx xx x', 'xxxxx'),
                ('x xx xxx xxxx\nxxxxx xxxx\nxxx xx xxxxxxxx', 'xxxxxxxx'),
                ]
    for (inString, solution) in testVals:
        val = longestWord(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
