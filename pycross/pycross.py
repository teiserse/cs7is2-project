import json


class Picross:
    """A class representing a picross puzzle (a.k.a a nonogram).

    Access the puzzle grid by puzzle[row][column].
    -1 means a slot is unknown.
    0 means a slot is (confirmed) empty.
    A number above 0 means a colour.
    """

    def __init__(self, width, height):
        self.rows = []
        self.columns = []
        self.width = width
        self.height = height
        self.puzzle = []
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
