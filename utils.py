import string

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]


def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x+y for x in A for y in B]
    

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# ***** UNCOMMENT TO RUN A DIAGONAL SUDOKU *****
# diag_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
# unitlist += diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def values2grid(values):
    """Convert the dictionary board representation to as string

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    """
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid):
    """Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.' or val == '0':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def check_sudoku_input(sudoku):
    if not len(sudoku)==81:
        return False, 'The sudoku input must contain exactly 81 chars'
    
    allowed_input = set(string.digits + '.')
    if not set(sudoku) <= allowed_input:
        return False, "The sudoku input must only contains digits and '.'"

    check_sudoku = grid2values(sudoku)
    rev_multidict = {}
    duplicates = []
    for unit in unitlist:
        for box in unit:
            if len(check_sudoku[box])==1:
                rev_multidict.setdefault(check_sudoku[box], set()).add(box)
        duplicates = [key for key, values in rev_multidict.items() if len(values) > 1]
        if len(duplicates)>0:
            return False, 'The sudoku input is erroneous: duplicate(s) in unit(s)'
        duplicates[:] = []
        rev_multidict.clear()
    
    return True, ''