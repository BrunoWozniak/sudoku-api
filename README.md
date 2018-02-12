# sudoku-api
Sudoku solver, constraint propagation, Python, Flask

# Introduction
This API is essentially a sudoku solver, submit an unresolved sudoku and get it back resolved

# Overview
The sudoku should be submitted as a string representing a concatenation of the 9 lines from left to right and from top to bottom, so, the string should be 81 chars long, the empty boxes should be represented by a '.' or '0'.

Example: ```'2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'```

The API also returns the resolution time in seconds.

Not yet available: I'm working on a extra parameter to use a combination of resolutions startegies (naked twins, naked triples, etc)

# Authentication
No authentication is required for the moment

# Error Codes
`200`: sudoku resolved

`400`: wrong input (length less than 81 or other chars than '.0123456789' or incorrect )

# Rate limit
I don't know how to do that yet...
