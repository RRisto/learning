# SISO program evaluateSatNoDummy.py

# Determine whether a particular Boolean formula is satisfied by a
# given truth assignment.

# inString: a string consisting only of 1's and 0's, in which the ith
# character is the truth value of variable x_i. Example: '101' means
# x_1 and x_3 are true but x_2 is false.

# returns: 'yes' if the particular Boolean formula given below in the
# program by the string booleanFormula is true with the given truth
# assignment, and 'no' otherwise.

# Example:
# >>> evaluateSatNoDummy('11')
# 'yes'

# Note: This program is identical to evaluateSat.py, except that the
# literal string 'dummy' is replaced with a real Boolean formula that
# can be evaluated. The file exists so we can test the program with a
# real Boolean formula.
import utils; from utils import rf
def evaluateSatNoDummy(inString):  
    # replace ``dummy'' with the desired formula
    booleanFormula = '(x1 OR NOT x2) AND (NOT x1 OR x2) AND (x1 OR NOT x1)'
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

def testEvaluateSat():
    testvals = [('11', 'yes'), 
                ('01', 'no'), 
                ]
    for (inString, solution) in testvals:
        val = evaluateSatNoDummy(inString)
        utils.tprint( inString, ":", val )
        assert val == solution

