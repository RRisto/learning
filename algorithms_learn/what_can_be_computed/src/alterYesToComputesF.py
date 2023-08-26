# SISO program alterYesToComputesF.py

# Ignore input, instead loading program P and input I from files
# progString.txt and inString.txt. We are also given some fixed
# functions F and G. If P(I)='yes', return F(I) and otherwise return
# G(I).

# inString: ignored

# returns: F(I) if P(I)='yes', otherwise G(I).

# Example:
# >>> utils.writeFile('progString.txt', rf('containsGAGA.py'))
# >>> utils.writeFile('inString.txt', 'TTGAGATT')
# >>> alterYesToComputesF('asdf') # see file F.py to understand F('asdf')
# '4'
#
# Note: The version printed in the textbook has a minor difference to
# the code below. The two lines "from F import F" and "from G import
# G" occur before the function definition in the printed version. The
# version given below works better in certain circumstances,
# especially when being simulated by universal.py.
import utils; from utils import rf
from universal import universal 
def alterYesToComputesF(inString):
    from F import F
    from G import G # G is any computable function different to F
    progString = rf('progString.txt') 
    newInString = rf('inString.txt') 
    val = universal(progString, newInString) 
    if val == 'yes':
        return F(inString) 
    else:
        return G(inString) 

def testAlterYesToComputesF():    
    from F import F
    from G import G # G is any computable function different to F
    F_input = 'xxxx'
    for (progName, inString, solution) in [('containsGAGA.py', 'GAGAGAGAG', F(F_input)), 
                                           ('containsGAGA.py', 'TTTTGGCCGGT', G(F_input)) ]:
        utils.writeFile('progString.txt', rf(progName))
        utils.writeFile('inString.txt', inString)
        val = utils.runWithTimeout(None, alterYesToComputesF, F_input)
        utils.tprint( (progName, inString), ":", val )  
        assert val == solution

