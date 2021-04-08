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


def perform_search(puzzle):
    pass
