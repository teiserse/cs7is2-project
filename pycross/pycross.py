import json
import os

class Picross:
    """
    A class representing a picross puzzle (a.k.a a nonogram).

    Access the puzzle grid by puzzle[row][column].
    -1 means a slot is unknown.
    0 means a slot is (confirmed) empty.
    A number above 0 means a colour.
    """

    def __init__(self, width, height):
        self.width = width  # width of the puzzle
        self.height = height  # height of the puzzle
        self.colours = {}  # colours used in the puzzle, indexed by the represented integer
        """
        Rows and columns are represented as a list of rows/columns. For rows, they are ordered
        going from up to down, and for columns they are ordered from left to right. 
        
        The rows/columns are defined as a list of tuples (colour, length).
        They represent the colours going from left to right on a row, and from up to down in a column.
        """
        self.rows = []
        self.columns = []

        self.puzzle = []  # The store of the current state of the puzzle
        for row in range(height):
            self.puzzle.append([])
            for column in range(width):
                self.puzzle[row].append(-1)

    def __str__(self):
        res = ""
        for row in self.puzzle:
            for column in row:
                if column == -1:
                    res += "?"
                else:
                    res += str(column)
            res += "\n"
        return res

    def __getitem__(self, item):
        """Returns the specified row of the puzzle.

        This actually accommodates all of the 2D operations
        since they all act on the row. As such, any time you
        call a 2D access (puzzle[row][column]), read or write,
        you are using __getitem__(row) on the puzzle first, and
        then __getitem__(column) or __setitem__(column, value)
        on the internal list.
        """
        return self.puzzle[item]

    def __setitem__(self, key, value):
        """Sets the specified row of the puzzle.

        The only way this is used is if for some reason we want
        to write an entire row by itself. In other cases, the
        call goes through __getitem__.
        """
        self.puzzle[key] = value

    def row_complete(self, index):
        """
        Function to check if a row is complete.
        """
        return self._check_complete(False, index)

    def column_complete(self, index):
        """
        Function to check if a column is complete.
        """
        return self._check_complete(True, index)

    def _check_complete(self, column, index):
        """
        Function to check is a particular row or column is complete.
        """
        line = []
        if column:
            line = [row[index] for row in self.puzzle]
        else:
            line = self.puzzle[index]

        rule = []
        if column:
            rule = self.columns[index]
        else:
            rule = self.rows[index]

        ser_line = _serialise_line(line)
        ser_line = [x for x in ser_line if x[0] != -1 and x[0] != 0]

        for i in range(len(ser_line)):
            if ser_line[i][0] != rule[i][0] and ser_line[i][1] != rule[i][1]:
                return False

        return len(ser_line) == len(rule)

    def get_possible_actions(self, index, row=True):
        """
        Function gathers information on puzzel and computes all permutations of a line given a row or column
        at a given index
        """
        constraints = self.columns[index]
        size = self.height
        if row:
            constraints = self.rows[index]
            size = self.width
        
        min = make_min(constraints, size)
        min_length = get_constraint_length(constraints)
        results = get_permutations(min, min_length, size)
        return results

    def get_possible_lines(self):
        """
        Function returns the lines that are not completed
        """
        possible_rows = []
        for i in range(self.height):
            if not self.row_complete(i):
                possible_rows.append(i)
        
        possible_cols = []
        for i in range(self.width):
            if not self.column_complete(i):
                possible_cols.append(i)
            
        possible_lines = [possible_rows, possible_cols]
        return possible_lines

def make_min(constraints, size):
    """
    Function makes the minimum line given a
    list of constraints and the length of the line
    """
    line = []
    min_length = get_constraint_length(constraints)
    for i in range(len(constraints)):
        fulls = constraints[i][1]
        for j in range(fulls):
            line.append(constraints[i][0])
        if i+1 < len(constraints):
            if constraints[i+1][0] == constraints[i][0]:
                line.append(0)

    if min_length < size:
        for i in range(size - min_length):
            line.append(0)
    return line

def rotate_list(l, num):
    """
    Function rotates a list l by num time.
    Function shift to the right
    """
    for i in range(num):
        temp = l.pop()
        l.insert(0, temp)
    return l

def get_index(min, min_length):
    """
    Function returns the positions of boundaries between constraints given a min line
    These indices are used to get permutations
    """
    temp = min
    index = []
    for i in range(min_length-1):
        if i+1 < len(min) and min[i] != min[i+1]:
            index.append(i+1)
    return index

def get_permutations(min, min_length, size):
    """
    Function recursively gets the permuations of a line given its min_length, line length and minimum line
    Returns a list of all lines possible
    """
    result = []
    result.append(min.copy())
    if min_length >= size:
        return result

    temp = min.copy()
    for i in range(size - min_length):
        temp = rotate_list(temp, 1)
        result.append(temp.copy())

    index = get_index(min, min_length)
    temp = min.copy()
    for i in index:
        temp.insert(i, 0)
        temp.pop()
        result = result + get_permutations(temp.copy(), min_length+1, size)
        temp = min.copy()

    return result

def get_constraint_length(constraint):
    """
    Function computes a the minimum length of given constriants
    Considers colour and number of blocks
    """
    sum = 0
    num_spaces = 0
    for i in range(len(constraint)):
        sum += constraint[i][1]
        if i+1 < len(constraint):
            if constraint[i+1][0] == constraint[i][0]:
                num_spaces += 1
    
    return sum + num_spaces

def from_json(json_string):
    """
    Helper function to create a Picross puzzle from a JSON file.
    See "example.json" for an example.
    """
    def as_picross(dct):
        if "picross" in dct:
            picross = Picross(dct["width"], dct["height"])
            picross.colours = dct["colours"]
            picross.rows = dct["rows"]
            picross.columns = dct["columns"]
            return picross
        return dct

    return json.loads(json_string, object_hook=as_picross)


def _serialise_line(line):
    """
    Helper function that reads a list, and returns a list of tuples of
    the array element, with the number of consecutive occurrences of
    the element, in the order of the original list
    """

    result = []
    for elem in line:
        if not result:
            result.append((elem, 1))
        else:
            (prev_elem, count) = result.pop()
            if elem == prev_elem:
                result.append((prev_elem, count + 1))
            else:
                result.append((prev_elem, count))
                result.append((elem, 1))

    return result
