# SISO program alterYoEToEoE.py

# Ignore input, instead loading program P from file progString.txt. If
# P('')='yes', return the empty string and otherwise return a nonempty
# string.

# inString: ignored

# returns: '' if P('')='yes', otherwise 'a non-empty string'.

# Example:
# >>> utils.writeFile('progString.txt', rf('containsGAGA.py'))
# >>> alterYoEToEoE('asdf')
# 'a non-empty string'
import utils; from utils import rf
from universal import universal
def alterYoEToEoE(inString):
    progString = rf('progString.txt')
    val = universal(progString, '')
    if val == 'yes':
        return '' # empty string
    else:
        return 'a non-empty string'

def testAlterYoEToEoE():
    testvals = [('containsGAGA.py', 'a non-empty string'),
                ('isEmpty.py', ''),
                ]
    for (progName, solution) in testvals:
        progString = rf(progName)
        utils.writeFile('progString.txt', progString)
        val = alterYoEToEoE('')
        utils.tprint(progName, ":", val)
        assert val == solution

