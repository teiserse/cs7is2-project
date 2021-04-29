import wx
import wx.grid
import backtrack, pycross

class GridFrame(wx.Frame, object):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Create a wxGrid object
        self.grid = wx.grid.Grid(self, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        self.grid.CreateGrid(10, 10)

        for row in range(10):
            self.grid.SetRowSize(row, 30)
            self.grid.SetColSize(row, 30)

    def setWhite(self,puzzle):
        for r in range(puzzle.height):
            for c in range(puzzle.width):
                self.grid.SetCellBackgroundColour(r,c,wx.WHITE)


    def setColour(self,puzzle):
        colours = []
        for item in puzzle.colours:
            colours.append(puzzle.colours[item])
        for colour in puzzle.colours.keys():
            for row in range(puzzle.height):
                for col in range(puzzle.width):
                    if puzzle[row][col] == colour:
                        self.grid.SetCellBackgroundColour(row,col,puzzle.colours[colour])

if __name__ == '__main__':
    puzzle = pycross.from_json(open("examples/5x5Coloured/camel.json").read())
    cs = backtrack.constraint_search(puzzle)
    app = wx.App(0)
    frame = GridFrame(None)
    frame.setWhite(cs)
    frame.setColour(cs)
    wx.Window.SetSize(frame,wx.DefaultCoord,wx.DefaultCoord,400,400)
    frame.Show()
    app.MainLoop()