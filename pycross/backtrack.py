from __future__ import print_function
import pycross

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


"""
Splits the rule pairs into separate row and colour lists
"""
def generate_row_rules(puzzle: pycross.Picross, row_index):
    row_rules = []; colour_rules = []
    for i in puzzle.rows[row_index]:
        row_rules.append(i[1])
        colour_rules.append(i[0])
    return row_rules, colour_rules

"""
Splits the rule pairs into separate column and colour lists
"""
def generate_column_rules(puzzle: pycross.Picross, column_index):
    column_rules = []; colour_rules = []
    for i in puzzle.columns[column_index]:
        colour_rules.append(i[0])
        column_rules.append(i[1])
    return column_rules, colour_rules

"""
Generates all possible permutations of a row
"""
def generate_rows(blocks, colours, length):
    if not blocks: return ["0" * length]
    if blocks[0] > length: return []

    starts = length - blocks[0]
    to_string = [str(int) for int in colours]

    if len(blocks) == 1:
        return [("0" * i + to_string[0] * blocks[0] + "0" * (starts - i)) for i in range(starts + 1)]

    ans = []
    for i in range(length - blocks[0]):
        for sol in generate_rows(blocks[1:], colours[1:], starts - i):
            ans.append("0" * i + to_string[0] * blocks[0] + sol)
    return ans

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
Helper function to convert the rows into lists of strings to integers
"""
def convert_rows(puzzle: pycross.Picross, index):
    row_rules, colour_rules = generate_row_rules(puzzle, index)
    ans = generate_rows(row_rules, colour_rules, puzzle.width)

    all_rows = []
    for t in ans:
        temp = []
        for each in t:
            temp.append(int(each))
        if row_filter(puzzle, temp) == True:
            all_rows.append(temp)
    return all_rows, index

"""
Checks to see if the column constraint is broken
For example, if the column was [1,3][1,2][2,3][3,4]
It sees if there are more than 5 colour '1s', or more than 3
colour '2s'. If there is, then we know that row combination cannot
lead to a solution and it will return True
"""

def constraint_check(puzzle: pycross.Picross):
    if type(puzzle.colours == int):
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
    possible_row, index = convert_rows(puzzle, 0)
    for r in possible_row:
        fringe.push([r, index])

    while not fringe.isEmpty():
        row, index = fringe.pop()
        solved_puzzle.__setitem__(index, row)

        """This is the backtracking here"""
        if constraint_check(solved_puzzle):
            continue
        if solved_puzzle.is_complete():
            return solved_puzzle
        elif index + 1 < puzzle.height:
            pr, i = convert_rows(puzzle, index + 1)
            for r in pr:
                fringe.push([r, index + 1])

    print('No solution found')
    return solved_puzzle


if __name__ == '__main__':
    puzzle = pycross.from_json(open("5x5.json").read())

    import time
    pre = time.perf_counter()
    cs = constraint_search(puzzle)
    post = time.perf_counter()
    print(post - pre)
    print(cs)