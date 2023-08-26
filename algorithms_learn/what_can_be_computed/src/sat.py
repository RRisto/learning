# SISO program sat.py

# Solves the computational problem Sat. In the textbook, Sat is
# described as a decision problem. This program, however, treats it as
# a general computational problem. If there is a positive solution
# then a description of a solution will be returned.  The recursive
# search algorithm enumerates all truth assignments and therefore
# requires exponential time in the worst case.

# inString: a Boolean formula B in CNF, expressed in ASCII as
# described in the textbook,
# e.g. '(x1 OR x2) AND (NOT x2 OR x3 OR x1)'

# returns: If B is satisfiable, a satisfying truth assignment will be
# returned, as a string consisting of the names of all true variables
# separated by commas. If B is not satisfiable, 'no' is returned. Note
# that the empty string does represent a satisfying assignment -- it
# assigns all variables to false (and this includes the possibility
# that there are no variables).

# Example:
# >>> sat('x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3')
# 'x3,x1'  [or another satisfying assignment]

import utils; from utils import rf
def sat(inString):

    # Convert the ASCII formula into our internal format for CNF
    # formulas. See the documentation of readSat() for details.
    cnfFormula = readSat(inString)

    # special case of zero clauses: solution is positive, but it's the empty string
    if len(cnfFormula)==0:
        return ''

    # dictionary mapping str to bool; key is the name of variable and
    # value is the truth value assigned to that variable
    truthAssignment = dict()

    # list of str, initialized to all variables in the formula
    remainingVariables = getVariablesAsList(cnfFormula)

    # Search for a satisfying assignment using recursion. See the
    # documentation of tryExtensions() for details.
    satisfyingAssignment = tryExtensions(cnfFormula, truthAssignment, remainingVariables)
    if satisfyingAssignment:
        trueVars = [var for var, truthVal in satisfyingAssignment.items() if truthVal]
        return ','.join(trueVars)
    else:
        return 'no'

def satisfies(cnfFormula, truthAssignment):
    """Return True if the given truthAssignment satisfies the given cnfFormula.

    Args:

        cnfFormula (list of dict -- see readSat() for details of this
            data structure): a CNF formula

        truthAssignment (dict mapping str to bool): keys are variable
            names and whose values are True or False. We do allow the
            possibility that not all variables are assigned by the
            truth assignment.

    Returns:

        bool: True if the given truthAssignment satisfies the given
            cnfFormula and False otherwise.

    """
    
    for clause in cnfFormula:
        clauseIsSatisfied = False
        for variable, posOrNeg in clause.items():
            if posOrNeg==1:
                if variable in truthAssignment and truthAssignment[variable] == True:
                    clauseIsSatisfied = True
                    break
            elif posOrNeg==-1: # i.e., the literal is negated
                if variable in truthAssignment and truthAssignment[variable] == False:
                    clauseIsSatisfied = True
                    break
            elif posOrNeg==0: # the literal appears both positive and negative
                if variable in truthAssignment:
                    clauseIsSatisfied = True
                    break
            else: # unexpected value
                assert False
        if not clauseIsSatisfied:
            return False
    return True

def testSatisfies():
    truthAssignment = {'x1':True, 'x2':True, 'x3':False}
    utils.tprint(truthAssignment)
    for (inString, solution) in [
            ('', True),
            ('x1', True),
            ('x1 AND (x2)', True),
            ('(x1) AND (NOT x2) AND (NOT x1)', False),
            ('(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)', False),
            ('x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3', True),
    ]:
        cnfFormula = readSat(inString)
        val = satisfies(cnfFormula, truthAssignment)
        utils.tprint(inString, val)
        assert val == solution


def getVariablesAsSet(cnfFormula):
    """Return a set of variables in the given formula.

    Args:

        cnfFormula (list of dict -- see readSat() for details of this
            data structure): a CNF formula

    Returns:

        set of str: the names of all variables that appear in
            cnfFormula

    """
    variables = set()
    for clause in cnfFormula:
        variables |= set(clause.keys())
    return variables

def getVariablesAsList(cnfFormula):
    """Return a list of variables in the given formula.

    Args:

        cnfFormula (list of dict -- see readSat() for details of this
            data structure): a CNF formula

    Returns:

        list of str: the names of all variables that appear in
            cnfFormula

    """
    return list(getVariablesAsSet(cnfFormula))

def testGetVariablesAsList():
    for (inString, solution) in [
            ('', []),
            ('x1', ['x1']),
            ('x1 AND (x2)', ['x1', 'x2']),
            ('(x1) AND (NOT x2) AND (NOT x1)', ['x1', 'x2']),
            ('(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)', ['x1', 'x2', 'x3']),
            ('x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3', ['x1', 'x2', 'x3']),
    ]:
        cnfFormula = readSat(inString)
        val = sorted(getVariablesAsList(cnfFormula))
        utils.tprint(inString, val)
        assert val == solution


def tryExtensions(cnfFormula, truthAssignment, remainingVariables):
    """Extend the given truth assignment to satisfy the given formula.

    This is the recursive function at the heart of finding a truth
    assignment for a given formula. If we can satisfy the given
    formula by extending the given truth assignment using the given
    remaining variables, a satisfying truth assignment is returned.
    The possible assignments are explored in true-first order,
    starting with the first variable in remainingVariables.

    Args:

        cnfFormula (list of dict -- see readSat() for details of this
            data structure): a CNF formula

        truthAssignment (dict mapping str to bool): keys are variable
            names and whose values are True or False. We do allow the
            possibility that not all variables are assigned by the
            truth assignment.

        remainingVariables (list of str): list of variables that have
            not yet been assigned a truth value.

    Returns:
    
        new truthAssignment (dict mapping str to bool): If it is
            possible to extend the given truthAssignment by assigning
            truth values to some or all of remainingVariables and thus
            satisfy cnfFormula, a satisfying truthAssignment will be
            returned. If there is no such truth assignment, None is
            returned.

    """
    if len(remainingVariables)==0:
        if satisfies(cnfFormula, truthAssignment):
            return truthAssignment
        else:
            return None

    nextVariable = remainingVariables[0]
    newRemainingVariables = remainingVariables[1:]

    # There are two recursive cases to deal with. In Case 1,
    # nextVariable is True. In Case 2, nextVariable is False.

    # Case 1 (nextVariable is True)
    newtruthAssignmentA = dict(truthAssignment)
    newtruthAssignmentA[nextVariable] = True

    satisfyingAssignment = tryExtensions(cnfFormula, newtruthAssignmentA, newRemainingVariables)
    if satisfyingAssignment:
        return satisfyingAssignment
    else:
        # Case 2 (nextVariable is False)
        newtruthAssignmentB = dict(truthAssignment)
        newtruthAssignmentB[nextVariable] = False
        return tryExtensions(cnfFormula, newtruthAssignmentB, newRemainingVariables)

def testTryExtensions():
    cnfFormula = readSat('x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3')
    utils.tprint('cnfFormula =', cnfFormula)
    for (truthAssignment, remainingVariables, isSatisfiable) in [
            (dict(), ['x1', 'x2', 'x3'], True),
            ({'x1':False}, ['x2', 'x3'], True),
            ({'x1':True}, ['x2', 'x3'], True),
            ({'x1':True, 'x2':True}, ['x3'], True),
            ({'x1':True, 'x3':False}, ['x2'], True),
            ({'x1':False, 'x3':False}, ['x2'], False),
            ({'x1':True, 'x2':False, 'x3':True}, [], True),
            ({'x1':False, 'x2':True, 'x3':False}, [], False),
            ({'x1':True, 'x2':False, 'x3':False}, [], True),
    ]:
        satisfyingAssignment = tryExtensions(cnfFormula, truthAssignment, remainingVariables)
        utils.tprint(truthAssignment, remainingVariables)
        utils.tprint('satisfyingAssignment =', satisfyingAssignment)
        if satisfyingAssignment:
            assert isSatisfiable
        else:
            assert not isSatisfiable
            
def readSat(inString):
    """Convert a string representing a CNF formula into a Python data
    structure representing the same formula.

    Convert a string representing a CNF formula into a Python data
    structure representing the same formula. The parameter inString
    must describe a CNF formula in the ASCII format described in the
    textbook. The returned object is in our internal format for
    storing a (CNF) SAT formula: it is list of clauses, where each
    clause is a dictionary whose keys are variable names (stored as
    strings) and values are +1 for positive literals and -1 for
    negative literals.

    Args:

        inString (str): a CNF formula in the ASCII format described in
            the textbook

    Returns:
    
        list of dict: This is our internal format for storing a (CNF)
            SAT formula. It is list of clauses, where each clause is a
            dictionary whose keys are variable names (stored as
            strings) and values are +1 for positive literals, -1 for
            negative literals, and 0 if the variable appears in the
            same clause both positively and negatively.

    """
    
    clauseStrings = inString.split('AND')
    clauseStrings = [x.strip() for x in clauseStrings]

    
    # Here we deal with an annoying special case. Unfortunately, our
    # spec for SAT instances doesn't distinguish very nicely between
    # empty clauses (which are unsatisfiable by definition), and an
    # empty *set* of clauses (which is satisfiable by definition).
    # Let us agree that if after the above splitting and stripping,
    # clauseStrings contains a single element which is the empty
    # string, then we have an empty set of clauses. Any other result
    # is a nonempty set of clauses, one or more of which may in fact
    # be an empty clause.
    if len(clauseStrings)==1 and clauseStrings[0]=='':
        clauseStrings = []

    clauseStrings = [x.strip('()') for x in clauseStrings]

    clauses = []
    for clauseString in clauseStrings:
        clause = dict()
        literals = clauseString.split('OR')
        literals = [x.strip() for x in literals]
        for literal in literals:
            if literal.startswith('NOT'):
                splitLiteral = literal.split()
                variableName = splitLiteral[1]
                if variableName not in clause:
                    clause[variableName] = -1
                elif clause[variableName] == 1:
                    clause[variableName] = 0
            elif len(literal)>0:
                variableName = literal
                if variableName not in clause:
                    clause[variableName] = 1
                elif clause[variableName] == -1:
                    clause[variableName] = 0
        clauses.append(clause)

        
    return clauses

def testReadSat():
    for (inString, numClauses, numVars) in [
            ('', 0, 0),
            ('  ', 0, 0),
            ('()', 1, 0),
            ('x1', 1, 1),
            ('x1 AND (x2)', 2, 2),
            ('x1 AND ()', 2, 1),
            ('x1 AND AND x2', 3, 2),
            ('  (  x1 )  AND x2 OR NOT   x3  ', 2, 3),
            ('(x1) AND (NOT x2) AND (NOT x1)', 3, 2),
            ('(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)', 4, 3),
    ]:
        utils.tprint('inString:', inString)
        cnfFormula = readSat(inString)
        utils.tprint('cnfFormula:', cnfFormula)
        assert len(cnfFormula) == numClauses
        assert len(getVariablesAsList(cnfFormula)) == numVars
    
def writeSat(cnfFormula):
    """Convert the given formula into an ASCII string description.

    Args:

        cnfFormula (list of dict -- see readSat() for details of this
            data structure): a CNF formula

    Returns:

        str: description of the formula as described in the textbook,
            e.g. '(x1 OR x2) AND (NOT x2 OR x3 OR x1)'

    """

    clauseStrings = [writeClause(clause) for clause in cnfFormula]
    return ' AND '.join(clauseStrings)

def writeClause(clause):
    """Convert the given clause into an ASCII string description.

    Args:

        clause (dict mapping str to +1,-1,0 -- see readSat() for
            details of this data structure): represents a clause. Each
            key is a variable name and the corresponding value is +1
            for positive literals, -1 for negative literals, and 0
            for both.

    Returns:

        str: description of the clause as described in the textbook,
            e.g. '(NOT x2 OR x3 OR x1)'

    """

    # There is no need to sort the variables, but it will give a more
    # readable and predictable outcome, since otherwise the order of
    # variables in the dictionary will be arbitrary.
    sortedClauseVariables = sorted(clause.keys())
    literalStrings = [writeLiteral(clause, variable) for variable in sortedClauseVariables]
    return '(' + ' OR '.join(literalStrings) + ')'

def writeLiteral(clause, variable):
    """Convert the given variable occurring in the given clause into an
    ASCII string description.

    Args:

        clause (dict mapping str to +1,-1,0 -- see readSat() for
            details of this data structure): represents a clause. Each
            key is a variable name and the corresponding value is +1
            for positive literals, -1 for negative literals, and 0
            for both.

        variable (str): name of the variable to be converted to its
            string description as a literal

    Returns:

        str: description of the literal as described in the textbook,
            e.g. 'NOT x2'

    """
    posNeg = clause[variable]
    if posNeg == 1:
        return variable
    elif posNeg == -1:
        return 'NOT ' + variable
    elif posNeg == 0:
        return variable + ' OR NOT ' + variable

def testWriteSat():
    for inString in ['', '   ', 'AND', 'x1 AND', '()',
                     'x1',
                     'x1 AND (x2)',
                     '(x1) AND (NOT x2) AND (NOT x1)',
                     '(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)',
                     'x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3'
                     'x1 OR NOT x1 OR x2 AND x3 OR NOT x3 OR NOT x3'
    ]:
        utils.tprint(inString)
        utils.tprint(writeSat(readSat(inString)), '\n\n')
        cnfString1 = inString
        cnfFormula1 = readSat(cnfString1)
        cnfString2 = writeSat(cnfFormula1)
        cnfFormula2 = readSat(cnfString2)
        assert cnfFormula1 == cnfFormula2

def testSat():
    for (inString, isSatisfiable) in [
            ('', True),
            ('   ', True),
            ('AND', False),
            ('x1 AND', False),
            ('()', False),
            ('x1', True),
            ('NOT x1', True),
            ('x1 AND (x2)', True),
            ('(x1) AND (NOT x2) AND (NOT x1)', False),
            ('(x1 OR x2) AND (NOT x2 OR x3 OR x1) AND (NOT x1)  AND (NOT x3 OR NOT x2)', False),
            ('x1 OR x3 AND NOT x1 OR NOT x2 OR NOT x3', True),
            ('x1 OR NOT x1 AND x1', True),
            ('x1 OR NOT x1 AND NOT x1', True),
    ]:
        satisfyingAssignment = sat(inString)
        utils.tprint('inString:', inString)
        utils.tprint('satisfyingAssignment:', satisfyingAssignment)
        utils.tprint('isSatisfiable:', isSatisfiable)
        if satisfyingAssignment != 'no':
            assert isSatisfiable
        else:
            assert not isSatisfiable
        
        
