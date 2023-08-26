# SISO program onlyZs.py

# returns: a string consisting of M copies of the character 'Z', where
# M is the number of 'Z' characters in the input.

# example:
# >>> onlyZs('aZbZZZc')
# 'ZZZZ'
import utils; from utils import rf
def onlyZs(inString):
    numZs = inString.count('Z')
    return 'Z' * numZs

def testOnlyZs():
    for (inString, solution) in [
            ('', ''),
            ('aassdc', ''),
            ('ZZZ', 'ZZZ'),
            ('Z', 'Z'),
            ('ascZsfaasZZsacscaZZZ', 'ZZZZZZ')
    ]:
        val = onlyZs(inString)
        utils.tprint(inString, ":", val)
        assert val == solution
        

