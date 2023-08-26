# SISO programs P1, P2, P3, P4

# These programs are used as examples in Chapter 7, demonstrating the
# difficulty in general of the computational problem ComputesIsEven.
import utils; from utils import rf
def P1(inString):    
    n = int(inString)
    if n%2==0: return 'yes'
    else: return 'no'

def P2(inString):
    if inString[-1] in '02468': return 'yes'
    else: return 'no'

def P3(inString):
    n = int(inString)
    if (2*n+1)%4==1: return 'yes'
    else: return 'no'

def P4(inString):
    n = int(inString)
    if (3*n+1)%5==1: return 'yes'
    else: return 'no'  


def testP1etc():
    testvals = [('0', 'yes'),
                ('2', 'yes'),
                ('4', 'yes'),
                ('100', 'yes'),
                ('1', 'no'),
                ('3', 'no'),
                ('5', 'no'),
                ('101', 'no'),
    ]

    for (inString, solution) in testvals:
        val = P1(inString)
        utils.tprint(inString, ':', val)
        assert val == solution
    
    for (inString, solution) in testvals:
        val = P2(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

    for (inString, solution) in testvals:
        val = P3(inString)
        utils.tprint(inString, ':', val)
        assert val == solution

    for (inString, solution) in testvals:
        val = P4(inString)
        utils.tprint(inString, ':', val)
        # no need to assert anything for P4
