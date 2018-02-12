import time, csv
from itertools import combinations
from utils import *


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """

    naked_twins_list = []
    for box in values.keys():
        if len(values[box]) == 2:
            for peer in peers[box]:
                if values[peer]==values[box]:
                    if not ([box, peer] in naked_twins_list or [peer, box] in naked_twins_list):
                        naked_twins_list.append([box, peer])

    for i in range(len(naked_twins_list)):
        box1 = naked_twins_list[i][0]
        box2 = naked_twins_list[i][1]
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        intersection = peers1 & peers2
        for box in intersection:
            if len(values[box])>2:
                for v in values[box1]:
                    values[box] = values[box].replace(v,'')
    
    return values


def naked_triples(values):
    """Eliminate values using the naked triplets strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked triplets eliminated from peers
    """
    # Naked triples strategy implemeted as per
    # http://www.sudokuwiki.org/naked_candidates
    for unit in unitlist:
        boxes_in_unit = [box for box in unit]
        for combo in combinations(boxes_in_unit, 3):
            combo_union_values = values[combo[0]] + values[combo[1]] + values[combo[2]]
            combo_unique_values = ''.join(set(combo_union_values))
            if len(combo_unique_values)==3:
                for box in set(unit)-set(combo):
                    if len(values[box])>2:
                        for v in combo_unique_values:
                            values[box]=values[box].replace(v,'')

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        # values = eliminate(values)
        # Use the Only Choice Strategy
        # values = only_choice(values)
        # Use the Naked Triples Strategy
        # values = naked_triples(values)
        # Use the Eliminate Strategy again
        values = eliminate(values)
        # Use the Only Choice Strategy again
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(grid2values(diag_sudoku_grid))
    start = time.clock()
    result = solve(diag_sudoku_grid)
    t = time.clock()-start
    print("Solved in %.3f sec"% t)
    # display(result)


    # solve_all(from_file("10k_sudoku.csv"), "sudoku", None)
    # solve_all(from_file("1m_sudoku.csv"), "sudoku", None)


    # try:
    #     import PySudoku
    #     PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    # except SystemExit:
    #     pass

    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
