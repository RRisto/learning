README.txt for WCBC materials version 1.1 (January 2019)
--------------------------------------------------------

1. Overview

WCBC is an abbreviation for the book "What Can Be Computed?: A Practical Guide to the Theory of Computation," written by John MacCormick and published by Princeton University Press (2018). Please see http://whatcanbecomputed.com for more details about the book. This directory contains supporting materials for WCBC. 

2. File types in this directory

The majority of the materials are Python programs (.py files), but there are several other file types, as summarized in the following table:

.cfg description of a context free grammar
.dfa description of a deterministic finite automaton
.nfa description of a nondeterministic finite automaton
.pda description of a push down automaton
.py  Python program or file (SISO or non-SISO -- see below)
.tm  description of a Turing machine
.txt ASCII text 

All the above file types are described in the WCBC book.

3. SISO and non-SISO Python files

WCBC defines a special kind of Python program referred to as "string in string out", or SISO for short. Please see the book for formal definitions and details, but the basic idea is that a SISO Python program defines at least one function. The first function appearing in the file is referred to as the "main" function, and this main function is required to receive only string parameters (usually exactly one string parameter) and it must also return a string. SISO programs are written with the goal of being as simple and clear as possible to readers of the book. Therefore, they are not object oriented, they do not usually attempt to use standard Python idioms, and they typically do not prioritize efficient or effective code.

In these materials, most but not all of the provided Python files are SISO Python programs; SISO programs are identified by a comment in the first line. There are also several non-SISO Python files. These include Python classes (e.g. graph.py, turingMachine.py) and the library of utility functions, utils.py.

4. Conventions for documenting Python files

SISO programs and non-SISO programs are documented via differing conventions. SISO programs are documented using #-style comments before the start of the main function. This is done to facilitate the incorporation of the function itself in the book: if standard Python docstrings were used instead, it would be more difficult to display SISO functions in the book. Non-SISO Python files are documented using standard Python docstrings.

5. Tests

In the vast majority of Python files, code for performing unit tests is placed in the same file as the code itself. Any function whose name begins with "test" is a test function. The test code is also useful for providing examples of how to invoke the other functions in the file.


6. Version history

version 1.0 (March 2018): Initial release

version 1.1 (January 2019): Minor bug fixes and corrections of typos; added Creative Commons license file.
