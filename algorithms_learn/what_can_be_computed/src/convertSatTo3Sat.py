# SISO program convertSatTo3Sat.py

# Convert an instance of SAT into an
# equivalent instance of 3-SAT.

# inString: an instance of SAT, formatted as described in the textbook
# and sat.py.

# returns: an instance of 3SAT in the same string format.

# Example:
# >>> convertSatTo3Sat('(x1 OR x2 OR NOT x3 OR NOT x4)')
# '(d1 OR x1 OR x2) AND (NOT d1 OR NOT x3 OR NOT x4)'
import utils; from utils import rf
import sat
def convertSatTo3Sat(inString):
    cnfFormula = sat.readSat(inString)
    allVariables = sat.getVariablesAsSet(cnfFormula)

    # Repeatedly sweep through the clauses looking for "long" clauses
    # (i.e., clauses with more than three literals). We favor
    # simplicity and readability over efficiency here. Every time a
    # long clause is found, it is removed, split, and replaced in the
    # list by two new, shorter clauses. The new clauses are inserted
    # at the point where the previous long clause was removed.  Then
    # we go back to the start of the entire list of clauses and start
    # looking for long clauses again.  This ends up being quadratic or
    # worse, whereas near-linear is possible. But the approach is
    # simple to understand and the clauses remain in a logical order.
    done = False
    while not done:
        done = True
        for clauseID in range(len(cnfFormula)):
            clause = cnfFormula[clauseID]
            if len(clause) > 3:
                done = False
                (newClause1, newClause2) = splitClause(clause, allVariables)
                cnfFormula.pop(clauseID)
                cnfFormula.insert(clauseID, newClause1)
                cnfFormula.insert(clauseID+1, newClause2)
                break

    return sat.writeSat(cnfFormula)

def splitClause(clause, allVariables):
    """Split a clause using the method described in the textbook.

    Args:

        clause (dict mapping str to int): Each key is a variable in
            the clause and the value is +1 for positive literals, -1
            for negative, 0 for both

        allVariables (set of str): A set of all variables in use, so
           that we can choose dummy variables that are not already in
           use.

    Returns:

        (clause, clause): 2-tuple consisting of two clauses, where
            each clause is a dictionary as described in the parameter
            above. The two clauses are the result of splitting the
            input using the method described in the textbook.

    """

    assert len(clause) > 3
    numLiterals = len(clause)
    dummyVariable = addDummyVariable(allVariables)
    # There is no need to sort the variables, but it will give a more
    # readable and predictable outcome, since otherwise the order of
    # variables in the dictionary will be arbitrary.
    sortedClauseVariables = sorted(clause.keys())
    newClause1 = dict()
    newClause2 = dict()
    # Put the first numLiterals-2 literals into newClause1, and the
    # last two literals into newClause2.
    for i in range(numLiterals):
        variable = sortedClauseVariables[i]
        posNeg = clause[variable]
        if i < numLiterals-2:
            newClause1[variable] = posNeg
        else:
            newClause2[variable] = posNeg
    # Add the dummy variable, positive in newClause1 and negative in newClause2
    newClause1[dummyVariable] = +1
    newClause2[dummyVariable] = -1

    return (newClause1, newClause2)

# Create, add, and return a new dummy variable name. Specifically, the
# set allVariables is a set of all current variable names. We find a
# new variable name of the form d1, d2, d3, ... which is not in the
# given set. The new name is added to the set, and the new name is also
# returned.  Implemented with a simple linear time algorithm; of
# course we could do better than that if desired.
def addDummyVariable(allVariables):
    """Create, add, and return a new dummy variable name.

    Specifically, the set allVariables is a set of all current
    variable names. We find a new variable name of the form d1, d2,
    d3, ... which is not in the given set. The new name is added to
    the set, and the new name is also returned.  Implemented with a
    simple linear time algorithm; of course we could do better than
    that if desired.

    Args:

        allVariables (set of str): A set of all variables in use, so
           that we can choose dummy variables that are not already in
           use.

    Returns:

        str: the new dummy variable name.

    """
    
    i = 1; done = False
    while not done:
        dummyName = 'd' + str(i)
        if dummyName not in allVariables:
            allVariables.add(dummyName)
            return dummyName
        i += 1


def testAddDummyVariable():
    formulaStr = '(x1 OR x2 OR NOT x3 OR NOT x4 OR x5) AND (NOT x1 OR NOT x2 OR x3 OR x4) AND (x4 OR NOT x5)'
    cnfFormula = sat.readSat(formulaStr)
    allVariables = sat.getVariablesAsSet(cnfFormula)
    numVars = len(allVariables)
    for i in range(5):
        dummyName = addDummyVariable(allVariables)
        utils.tprint(dummyName, allVariables)
        varName = 'd'+str(i+1)
        assert varName in allVariables
        assert len(allVariables) == numVars + i+1

def testSplitClause():
    formulaStr = '(x1 OR x2 OR NOT x3 OR NOT x4 OR x5) AND (NOT x1 OR NOT x2 OR x3 OR x4) AND (x4 OR NOT x5)'
    cnfFormula = sat.readSat(formulaStr)
    allVariables = sat.getVariablesAsSet(cnfFormula)
    result = splitClause(cnfFormula[0], allVariables)
    solution = ({'x1': 1, 'd1': 1, 'x3': -1, 'x2': 1}, {'d1': -1, 'x5': 1, 'x4': -1})
    utils.tprint('before split:', cnfFormula[0], '\nafter split:', result)
    assert result==solution
    
def testConvertSatTo3Sat():
    s0 = '(x1 OR x2 OR NOT x3 OR NOT x4 OR x5) AND (NOT x1 OR NOT x2 OR x3 OR x4) AND (x4 OR NOT x5)'
    s0soln = '(d1 OR d2 OR x1) AND (NOT d2 OR x2 OR NOT x3) AND (NOT d1 OR NOT x4 OR x5) AND (d3 OR NOT x1 OR NOT x2) AND (NOT d3 OR x3 OR x4) AND (x4 OR NOT x5)'
    s1 = ''
    s1soln = ''
    s2 = 'x1'
    s2soln = '(x1)'
    s3 = 'x1 AND NOT x2'
    s3soln = '(x1) AND (NOT x2)'
    s4 = 'x1 OR NOT x2'
    s4soln = '(x1 OR NOT x2)'

    testvals = [
        (s0, s0soln),
        (s1, s1soln),
        (s2, s2soln),
        (s3, s3soln),
        (s4, s4soln),
    ]

    for (inString, soln) in testvals:
        utils.tprint('**', inString, '**')
        converted = convertSatTo3Sat(inString)
        utils.tprint(converted, '\n\n')
        assert converted == soln

