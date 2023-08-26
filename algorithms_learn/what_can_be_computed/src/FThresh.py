# A dummy function provided so that threshToOpt compiles.  FThresh
# should really be the threshold version of an optimization problem F.
import utils; from utils import rf
def FThresh(inString, threshold):
    pass


def testFThresh():
    val = FThresh('abc', 5.7)
    assert val == None
