import json
from functools import cache
# We're doing a lot of iterating over lists over and over again, and just return the result:
# So, if something is immutable (e.g. something derived from the line rules
# but not the board state), we can use the @cache decorator to cache and optimise the result.
# But this won't work on anything that depends on board state (i.e. filled in tiles)


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
        
        guide (works both for rows and columns):
        self.rows = the list of rows
        self.rows[row] = the list of rules in the row
        self.rows[row][rule] = a rule in the row, can be a 2-ple or 2 element list
        self.rows[row][rule][0] = the rule's colour
        self.rows[row][rule][1] = the rule's length
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

    def is_complete(self):
        for row in range(self.height):
            if not self.is_row_complete(row):
                return False

        for column in range(self.width):
            if not self.is_column_complete(column):
                return False

        return True

    @cache
    def row_has_colour(self, row_index, colour):
        """
        Checks if a row has a particular colour -
        i.e. can you use that colour in this row.
        """
        line = self.rows[row_index]
        for rule in line:
            if rule[0] == colour:
                return True

        return False

    @cache
    def column_has_colour(self, column_index, colour):
        """
        Checks if a column has a particular colour -
        i.e. can you use that colour in this column.
        """
        line = self.columns[column_index]
        for rule in line:
            if rule[0] == colour:
                return True

        return False

    def is_row_complete(self, index):
        """
        Function to check if a row is complete.
        """
        return self._check_complete(False, index)

    def is_column_complete(self, index):
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
            if i >= len(rule):
                return False
            if ser_line[i][0] != rule[i][0] or ser_line[i][1] != rule[i][1]:
                return False

        return len(ser_line) == len(rule)


def from_json(json_string):
    """
    Helper function to create a Picross puzzle from a JSON file.
    See the "examples" folder for examples.
    """
    def as_picross(dct):
        if "picross" in dct:
            picross = Picross(dct["width"], dct["height"])
            colours = {int(number): description for number, description in dct["colours"].items()}
            picross.colours = colours
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
