import pycross
import time

class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self, item):
        """Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        return self.list.pop()

    def isEmpty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0


"""
This function cuts out some rows that are impossible
i.e. column doesn't have that colour 
(is this constraint propagation?)
"""
def row_filter(puzzle: pycross.Picross, row):
    for c in range(puzzle.width):
        if row[c] == 0: continue
        elif not puzzle.column_has_colour(c, row[c]): return False
        else: return True

"""
Helper function that returns the filtered rows
"""
def convert_rows(puzzle: pycross.Picross, index):
    ans = puzzle.get_possible_lines(index, True)
    all_rows = []
    for t in ans:
        if row_filter(puzzle, t) == True:
            all_rows.append(t)
    return all_rows, index

"""
Checks to see if the column constraint is broken
For example, if the column was [1,3][1,2][2,3][3,4]
It sees if there are more than 5 colour '1s', or more than 3
colour '2s'. If there is, then we know that row combination cannot
lead to a solution and it will return True
"""
def constraint_check(puzzle: pycross.Picross):
    if type(puzzle.colours) == int:
        for c in range(puzzle.width):
            counter = 0
            summation = 0
            for r in range(puzzle.height):
                if puzzle[r][c] == puzzle.colours:
                    counter += 1
            pairs = puzzle.columns[c]
            for item in pairs:
                summation += item[1]
            if counter > summation:
                return True

    else:
        for colour in puzzle.colours:
            for c in range(puzzle.width):
                counter = 0
                summation = 0
                for r in range(puzzle.height):
                    if puzzle[r][c] == colour:
                        counter += 1
                pairs = puzzle.columns[c]
                for item in pairs:
                    summation += item[1]
                if counter > summation:
                    return True

"""
Using depth first search to find a solution for the nonogram
We backtrack though if the current row combinations break 
any constraints
"""
def constraint_search(puzzle: pycross.Picross):
    if puzzle.is_complete(): return puzzle
    
    solved_puzzle = puzzle
    fringe = Stack()
    empty_row = []
    for i in range(puzzle.width):
        empty_row.append(-1)

    possible_row, index = convert_rows(puzzle, 0)
    for r in possible_row:
        fringe.push([r, index])

    while not fringe.isEmpty():
        
        if solved_puzzle.is_complete():
            for row in range(puzzle.height):
                for column in range(puzzle.width)
                    if puzzle[row][column] == -1:
                        puzzle[row][column] = 0
            return solved_puzzle

        row, index = fringe.pop()
        solved_puzzle.__setitem__(index, row)

        for i in range(index + 1, puzzle.height):
            solved_puzzle.__setitem__(i, empty_row)

        if constraint_check(solved_puzzle):
            for i in range(puzzle.height):
                if i > index:
                    solved_puzzle.__setitem__(i, empty_row)
            continue

        if index + 1 < puzzle.height:
            pr, i = convert_rows(puzzle, index + 1)
            for r in pr:
                fringe.push([r, i])

    print('No solution found')
    return solved_puzzle


if __name__ == '__main__':
    puzzle = pycross.from_json(open("Nonograms/5x5Mono/clock.json").read())
    pre = time.perf_counter()
    cs = constraint_search(puzzle)
    post = time.perf_counter()
    print(post - pre)
    print(cs)
