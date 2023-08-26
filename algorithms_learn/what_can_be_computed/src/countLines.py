import utils; from utils import rf
def countLines(inString):          
    # split on newlines
    lines = inString.split('\n')
    # return the number of lines, as a string
    return str(len(lines))         
