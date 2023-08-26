# SISO program threshToOpt.py

# Given a method of solving a threshold problem FThresh, solve the
# corresponding optimization problem FOpt. (See exercise 4.16 for
# details.)

# In this implementation, FOpt is actually a *minimization* problem.

# As described in the book, we assume the objective function V(I,S)
# for the threshold and optimization problems is integer-valued. In
# this implementation, we also assume V(I,S) is non-negative.

# inString: instance I of FOpt to be solved

# upperBound: string representing an integer that is an upper bound
# (over S) for V(I,S).

# returns: instance S' such that V(I,S') is minimized.

# Example: see the test function below for an example.

import utils; from utils import rf
# Import a function solving the threshold version of the optimization
# problem FOpt.
from FThresh import FThresh 
def threshToOpt(inString, upperBound):
    lowerBound = 0
    upperBound = int(upperBound)

    # Check initial bounds to see if binary search is necessary.
    lowerResult = FThresh(inString, str(lowerBound))
    upperResult = FThresh(inString, str(upperBound))
    if lowerResult != 'no': return lowerResult
    if upperResult == 'no': return 'no'

    # Optimal value is somewhere between upper and lower bounds, so
    # begin binary search.  We maintain the invariant that the lower
    # bound always yields a negative instance and the upper bound
    # always yields a positive instance.
    while lowerBound < upperBound - 1:
        midVal = int( (upperBound+lowerBound)/2 )
        midResult = FThresh(inString, str(midVal))
        if midResult == 'no':
            lowerBound = midVal
        else:
            upperBound = midVal
    return FThresh(inString, str(upperBound))  

# Let min be the optimization problem that accepts a list of
# nonnegative integers and returns the smallest. We define a threshold
# version of this problem, minThresh, which returns any element of the
# list no greater than the given threshold. This will be used for
# testing the above threshToOpt function.
def minThresh(inString, threshold):
    vals = [int(x) for x in inString.split()]
    threshold = int(threshold)
    for v in vals:
        if v <= threshold:
            return str(v)
    return 'no'

def testThreshToOpt():
    global FThresh
    FThresh = minThresh
    inStrings = [\
                 '13 18 16 35 23 19 42 73 4 13 8 22',\
                 '',\
                 '0',\
                 '0 1 2 3',\
                 '4',\
                 '4 4 4',\
                 '7 6 5 4',\
                 '4 5',\
                 '4 5 6',\
                 '5',\
                 '5 6',\
                 '5 6 7',\
                 '105 106 107',\
                 '100 105 106 107',\
                 ]
    upperBound = 100
    for inString in inStrings:
        val = threshToOpt(inString, upperBound)
        utils.tprint('with upper bound', upperBound, ', min of', inString, ':', val)
        nums = [int(x) for x in inString.split()]
        if len(nums)==0 or min(nums) > upperBound:
            solution = 'no'
        else:
            solution = str(min(nums))
        assert val == solution

