import json


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
        
        The rows/columns are defined as a list of tuples (colour, length). They represent the colours
        going from left to right on a row, and from up to down in a column.
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


def from_json(json_string):
    def as_picross(dct):
        print(dct)
        if "picross" in dct:
            picross = Picross(dct["width"], dct["height"])
            picross.colours = dct["colours"]
            picross.rows = dct["rows"]
            picross.columns = dct["columns"]
            return picross
        return dct
    return json.loads(json_string, object_hook=as_picross)
