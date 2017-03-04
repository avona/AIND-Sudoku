import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# Find all instances of naked twins
# Eliminate the naked twins as possibilities for their peers
def naked_twins(values):
    
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # auxiliary dictionary for tracking occurrences of twins in certain unit
    twins_list = {}
    
    # loop trough each unit and then each box in that unit
    for unit in unitlist:
        #for box in unit:
            # filter boxes with only two digits, then populate auxiliary dictionary
            # while counting the number of boxes with identical values: {'23':2, '17':4,'32':1,...}

        twins_list = count_vals(values, unit)
        # check if unit has at least one box with two digits
        if twins_list:
            # iterate through each found box with two digits 
            find_and_delete_twins(values, twins_list, unit)

        # empty the auxiliary dictionary for the next unit
        twins_list = {}

    return values


def find_and_delete_twins(values, twins_list, unit):
    for counter in twins_list:
        # check if a unit has at least 2 boxes with the same two digits, i.e. find twins
        if twins_list[counter] == 2:
            # iterate through eeach box in the unit and delete corresponding values
            for b in unit:
                delete_twins(values, counter, b)


def delete_twins(values, counter, b):
    # make sure we don't delete the values from twins!
    if values[b] != counter:
        # delete values found in twins from the peers in a given unit
        for i in [0,1]:
            if counter[i] in values[b]:
                assign_value(values, b, values[b].replace(counter[i],''))    


def count_vals(values, unit):
    count_list = {}
    for box in unit:
        if len(values[box]) == 2:
            if values[box] in count_list:
                count_list[values[box]] += 1
            else:
                count_list[values[box]] = 1
    return count_list


rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# added contraint that considers diagonals too
diagonal_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows,reversed(cols))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# converts string into dictionary and fills empty boxes with all possible values
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #print(diagonal_units)
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

# displays sudoku in traditional format
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

# eliminates values from peers if a certain box has been solved,
# i.e. contains only one digit and returns a new/reduced grid
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

# updates a certain box with a single value if there is the only value 
# that can be placed to that box in the given unit, and returns a new/reduced grid
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

# returns new/reduced grid after different solution strategies were applied
# or False if there is no further reductions and reductions reached incorrect solution 
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # apply eliminate strategy
        values = eliminate(values)
        # apply only_choice strategy
        values = only_choice(values)
        # apply naked_twins strategy
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


# search for solution by recursively reducing the grid and branching out on
# possible solution by choosing a box with the fewest values in it.
# returns False if there is no solution or solved grid in the opposite case
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    
    if all(len(values[i]) == 1 for i in boxes):
        return values
        
    # Choose one of the unfilled squares with the fewest possibilities
    for b in boxes:
        if len(values[b]) > 1:
            fewest_choices_box = b
            break
            
    for box in boxes:
        if len(values[box]) > 1:
            if len(values[box]) < len(values[fewest_choices_box]):
                fewest_choices_box = box
    
    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for digit in values[fewest_choices_box]:
        new_values = values.copy()
        new_values[fewest_choices_box] = digit
        final_values = search(new_values)
        if final_values:
            return final_values

# main solution function that calls grid_values funtion that converts a given
# string into a dictionary populated with all possible values
# returns solved grid or False otherwise
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
