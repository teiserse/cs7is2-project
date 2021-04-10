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

    # Prepare start
    # is it already solved?
    if puzzle.is_complete():
        return puzzle

    # set up the first set of actions
