from queue import PriorityQueue
import pycross


# notes
# - start with a dumb queue and go from there.
# - check the a* notes to figure out a good heuristic.
# - hold up - if the action to draw any square is the same, is this even a*?
# can we skip that step and do greedy first search?
# or maybe we can do some weird thing with the action weight?
# - remember - this is not going to be good because search is bad for this type of thing.
# - Encode the solution as a set of filling in because order doesn't matter? also avoids directly needing the 2D grid
# - - a tuple of (x, y, colour)?
# - currently will be fed in an empty puzzle. Might be changed later in order to take in half-complete ones
# or even potentially wrongly filled ones (the last one will be quite hard, but possible?).


def perform_search(puzzle: pycross.Picross):
    # Setup
    frontier = PriorityQueue()
    already_input = set()

    # Prepare start
    # is it already solved?
    if puzzle.is_complete():
        return puzzle

    # set up the first set of actions
    for row in range(puzzle.height):
        for column in range(puzzle.width):
            for colour in puzzle.colours.keys():
                filled_tiles = set()
                filled_tiles.add((row, column, colour))
                frontier.put((1, filled_tiles))
                already_input.add(frozenset(filled_tiles))

    # Begin search
    found = False
    while not found:
        # get the set of used tiles
        _weight, inputs = frontier.get()
        # set up the game board
        # also, get the set of covered tiles
        used_tiles = set()
        for item in inputs:
            row, column, colour = item
            puzzle[row][column] = colour
            used_tiles.add((row, column))
        # check if it is solved
        if puzzle.is_complete():
            found = True
            break
        # if not solved, reset the board
        for item in inputs:
            row, column, _ = item
            puzzle[row][column] = -1
        # add to the frontier
        for row in range(puzzle.height):
            for column in range(puzzle.width):
                for colour in puzzle.colours.keys():
                    if (row, column) not in used_tiles:
                        new_inputs = inputs.copy()
                        new_inputs.add((row, column, colour))
                        if frozenset(new_inputs) not in already_input:
                            frontier.put((len(new_inputs), new_inputs))
                            already_input.add(frozenset(new_inputs))
        if frontier.empty():
            print("No Solution Found")
            found = True

    # found solution
    return puzzle


if __name__ == '__main__':
    x = pycross.Picross(5, 2)
    x.colours = {1: "black"}
    x.rows = [[[1, 2], [1, 2]], [[1, 5]]]
    x.columns = [[[1, 2]], [[1, 2]], [[1, 1]], [[1, 2]], [[1, 2]]]
    y = perform_search(x)
    print(y)
