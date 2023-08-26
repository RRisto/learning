# An example of a program that enters an infinite loop, as discussed
# in Chapter 2.
import utils; from utils import rf
def infiniteLoop(inString): 
    x = 1
    while x > 0:
        x = x + 1
    return str(x)  


def testinfiniteLoop():
    inString = 'asdf'
    val = utils.runWithTimeout(None, infiniteLoop, inString)
    assert val == None
