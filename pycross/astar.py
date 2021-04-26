from queue import PriorityQueue
import pycross
from functools import lru_cache


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


def portion_of_possibles_heuristic(puzzle):
    """
    For the heuristic values, we look into how many of the possible
    variants of a line/column can we complete right now.

    The higher number of possibilities that remain, the farther
    away we are from a potential solution?

    Or would we potentially want to reward a more general answer?
    like if we have a line of 3 and current state of ??1??, that's the best
    option (guaranteed, actually), so that should qualify as some sort of
    free action?

    It's hard to say if we're actually doing filtering or some such at this point
    """
    pass


if __name__ == '__main__':
    x = pycross.from_json(open("examples/5x5Monochrome/1.json").read())

    import time
    pre = time.perf_counter()
    y = perform_search(x, cost_mul_function)
    post = time.perf_counter()
    print(post - pre)
    print(y)
