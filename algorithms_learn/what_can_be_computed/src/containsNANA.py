# SISO program containsNANA.py

# Return 'yes' if the input contains any of the substrings 'CACA',
# 'GAGA', 'TATA', 'AAAA'. Otherwise return 'no'.

# inString: the string to be searched

# returns: 'yes' if the input contains any of the substrings 'CACA',
# 'GAGA', 'TATA', 'AAAA'. Otherwise return 'no'

# Example:
# >>> containsNANA('CCCCCCGAGATTTATA')
# 'yes'
import utils; from utils import rf
def containsNANA(inString):  
    strings = ['CACA', 'GAGA', 'TATA', 'AAAA']
    for string in strings:
        if string in inString:
            return 'yes'
    return 'no'  

def testContainsNANA():
    numTests = 25
    strings = ['CACA', 'GAGA', 'TATA', 'AAAA']
    for i in range(numTests):
        randStr = utils.randomString('abcdef')
        val = containsNANA(randStr)
        utils.tprint(randStr, ':', val)
        assert val == 'no'
        for string in strings:
            if i==0:
                insertLoc = 0
            elif i==1:
                insertLoc = len(randStr)
            else:
                insertLoc = utils.aRandom.randint(0, len(randStr))
            inString = randStr[:insertLoc] + string + randStr[insertLoc:]
            val = containsNANA(inString)
            utils.tprint(inString, ':', val)
            assert val == 'yes'
            
