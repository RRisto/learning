# SISO program crashOnSelf.py

# This is a placeholder program that would solve the problem
# CrashOnSelf *if* there existed a working implementation of
# crashOnString. In fact, of course, neither of these programs can
# work as intended since they both attempt to solve uncomputable
# problems.
import utils; from utils import rf
from crashOnString import crashOnString  
def crashOnSelf(progString):   
    return crashOnString(progString, progString) 


def testcrashOnSelf():
    # There is nothing meaningful to assert in this test, because
    # crashOnString is an oracle function that does nothing in our
    # implementation.
    crashOnSelf('asdf')
