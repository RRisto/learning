# SISO program loop.py

# This program ignores its input and enters an infinite loop.
import utils; from utils import rf
def loop(inString):
    utils.loop()


def testLoop():
    inString = 'asdf'
    val = utils.runWithTimeout(None, loop, inString)
    
