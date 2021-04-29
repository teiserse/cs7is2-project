import wx
import wx.grid
import backtrack, pycross

class GridFrame(wx.Frame, object):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(10, 10)

        for row in range(10):
            self.grid.SetRowSize(row, 30)
            self.grid.SetColSize(row, 30)

    def setWhite(self,puzzle):
        for r in range(puzzle.height):
            for c in range(puzzle.width):
                self.grid.SetCellBackgroundColour(r,c,wx.WHITE)

    def set_colour(self, puzzle):
        colour_dict = pycross.from_json(open("colourDict.json").read())
        colours = puzzle.colours
        for key in colours:
            for colour_def in colour_dict.keys():
                if colours[key] == colour_def:
                    for row in range(puzzle.height):
                        for col in range(puzzle.width):
                            if puzzle[row][col] == key:
                                self.grid.SetCellBackgroundColour(row,col,colour_dict[colour_def])

if __name__ == '__main__':
    puzzle = pycross.from_json(open("examples/WxHColoured/brocolli.json").read())
    cs = backtrack.constraint_search(puzzle)
    app = wx.App(0)
    frame = GridFrame(None)
    frame.setWhite(cs)
    frame.set_colour(cs)
    wx.Window.SetSize(frame,wx.DefaultCoord,wx.DefaultCoord,400,400)
    frame.Show()
    app.MainLoop()