# SISO program evaluateSat.py

# Determine whether a particular Boolean formula is satisfied by a
# given truth assignment. The program does not work as written
# below. The string 'dummy' needs to be replaced with a real Boolean
# formula before it can function.

# inString: a string consisting only of 1's and 0's, in which the ith
# character is the truth value of variable x_i. Example: '101' means
# x_1 and x_3 are true but x_2 is false.

# returns: 'yes' if the particular Boolean formula pasted in to
# replace 'dummy' is true with the given truth assignment, and 'no'
# otherwise.

# Note: See evaluateSatNoDummy.py for an example of how this program
# can be altered to work correctly for a particular Boolean formula.
import utils; from utils import rf
def evaluateSat(inString):  
    # replace ``dummy'' with the desired formula
    booleanFormula = 'dummy' 
    clauses = booleanFormula.split('AND')
    # return ``yes'' iff the clauses are all satisfied by the given inString
    # ...   
    # remove whitespace and parentheses from clauses
    clauses = [x.strip() for x in clauses]
    clauses = [x.strip('()') for x in clauses]
##    print(clauses)
    for clause in clauses:
        literals = clause.split('OR')
        # remove whitespace
        literals = [x.strip() for x in literals]
##        print(literals)
        clauseIsSatisfied = False
        for literal in literals:
            if literal.startswith('NOT'):
                negated = True
                splitLiteral = literal.split()
                variableName = splitLiteral[1]
            else:
                negated = False
                variableName = literal
            variableID = int(variableName[1:]) # ignore the initial ``x'' in the variable name
            binaryInput = inString[variableID-1] # variable IDs start at 1 not 0
            if (binaryInput=='1' and not negated) or (binaryInput=='0' and negated):
                clauseIsSatisfied = True
                # this clause is satisfied, no need to check remaining literals
##                print ('clause satisfied by', literal)
                break 
##            print ( negated, variable, variableID)
        if not clauseIsSatisfied:
            # this clause is unsatisfied, so no need to check remaining clauses
##            print ('clause is not satisfied')
            return 'no'
    # all clauses were satisfied
    return 'yes'

#####################
# For tests, see the almost identical file evaluateSatNoDummy.py
#####################

