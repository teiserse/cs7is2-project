from queue import PriorityQueue
import pycross


# This originally started as an attempt to define a-star search,
# But due to the difficulty of defining a sensible and usable heuristic,
# The extenuating circumstances under which we are working in,
# And the fact that *nothing* can stop this method from sucking anyway,
# We ended up not writing a heuristic and just running a uniform cost search.

def perform_search(puzzle: pycross.Picross, cost_function=None, heuristic_function=None):
    """
    Perform a solution search over the puzzle.
    If no cost function is provided, all moves have same cost of 1.
    If no heuristic is provided, heuristic is always 0 (no heuristic used).
    """
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
                # filter out invalid moves
                if not puzzle.row_has_colour(row, colour) or not puzzle.column_has_colour(column, colour):
                    continue
                # and if the move is valid:
                filled_tiles = set()
                filled_tiles.add((row, column, colour))
                cost = 1
                if cost_function is not None:
                    cost = cost_function(puzzle, (row, column, colour))
                frontier.put((cost, filled_tiles))
                already_input.add(frozenset(filled_tiles))

    # Begin search
    found = False
    while not frontier.empty():
        # get the set of used tiles
        weight, inputs = frontier.get()
        prev_cost = weight

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

        # if using heuristic, remove previous heuristic to get past move costs

        # add to the frontier
        for row in range(puzzle.height):
            for column in range(puzzle.width):
                for colour in puzzle.colours.keys():
                    # filter out invalid moves
                    if not puzzle.row_has_colour(row, colour) or not puzzle.column_has_colour(column, colour):
                        continue
                    # and if the move is valid:
                    if (row, column) not in used_tiles:
                        new_inputs = inputs.copy()
                        new_inputs.add((row, column, colour))
                        if frozenset(new_inputs) not in already_input:
                            cost = len(new_inputs)
                            if cost_function is not None:
                                cost = prev_cost + cost_function(puzzle, (row, column, colour))
                            frontier.put((cost, new_inputs))
                            already_input.add(frozenset(new_inputs))

        # if not solved, reset the board
        for item in inputs:
            row, column, _ = item
            puzzle[row][column] = -1

    if not found:
        print("Solution Not Found.")

    # return solved puzzle (if found) or reset puzzle (if not found)
    return puzzle


def cost_additive_function(puzzle: pycross.Picross, move):
    """
    A cost function which adds together a score from the row and the column
    of the input move, based on the proportion of the row/column that is
    the the colour of the move.

    the row/column contributes a score of 0 to 1 - the number of squares of that
    colour in the row/column divided by the length of the row/column -
    higher score means higher probability.
    Then, we take the score away from 1, as a better option means a lower cost.

    A full row and column intersecting should give a 0 cost move, while a more sparse
    move will give a higher one, at a limit approaching 2 (2 would mean both the row
    and column give 0, meaning it is an invalid move and should not be considered to begin with)

    Cost function range: [0, 2)
    """
    row, column, colour = move

    row_cost = 1 - puzzle.row_colour_proportion(row, colour)
    column_cost = 1 - puzzle.column_colour_proportion(column, colour)

    return row_cost + column_cost


def cost_mul_function(puzzle: pycross.Picross, move):
    """
    A cost function which multiples together a score from the row and the column
    of the input move, based on the proportion of the row/column that is
    the the colour of the move.

    the row/column contributes a score of 0 to 1 - the number of squares of that
    colour in the row/column divided by the length of the row/column -
    higher score means higher probability.
    Then, we take the score away from 1, as a better option means a lower cost.

    A full row and column intersecting should give a 0 cost move, while a more sparse
    move will give a higher one, at a limit approaching 1 (1 would mean both the row
    and column give 0, meaning it is an invalid move and should not be considered to begin with)

    Cost function range: [0, 1)
    """
    row, column, colour = move

    row_cost = 1 - puzzle.row_colour_proportion(row, colour)
    column_cost = 1 - puzzle.column_colour_proportion(column, colour)

    return row_cost * column_cost


if __name__ == '__main__':
    x = pycross.from_json(open("examples/5x5Monochrome/1.json").read())

    import time

    pre = time.perf_counter()
    y = perform_search(x, cost_mul_function)
    post = time.perf_counter()
    print(post - pre)
    print(y)
