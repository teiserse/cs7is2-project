"""
Script in order to run tests on the project files.
"""
import sys
import os
import argparse
import functools
import time

import pycross
import astar

parser = argparse.ArgumentParser(description="Run test cases on the algorithms made for the project.")
parser.add_argument('-a', '--algorithm', choices=["astar", "all"], required=True, help="which algorithm(s) to run")
parser.add_argument('-t', '--testcase', required=True, help="which testcase(s) to run")

args = parser.parse_args()

print(f"Selected algorithm: {args.algorithm}")

# Do extra things to select algorithm here
# for now only tests astar
test_function = functools.partial(astar.perform_search, cost_function=astar.cost_mul_function)

# set the cwd to the python files, in case the script
# is called from a different cwd.
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Get the lists of the example filenames
example_sets = os.scandir("examples")
example_dict = dict()
for ex_set in example_sets:
    tests = [f.path for f in os.scandir(ex_set.path) if f.path.endswith(".json")]
    example_dict[ex_set.name] = tests

# Go through the filenames
for test_set, test_cases in example_dict.items():
    # get the testsets that start with the testcase name
    # will improve later
    if test_set.startswith(args.testcase):
        print(f"Running {test_set}:")
        for case in test_cases:
            print(f"Loading {case}...")
            # Import the puzzle (probably want to do error checks on this)
            curr_puzzle = pycross.from_json(open(case).read())
            print(f"Beginning test on {case}...")
            # Start solving!
            pre = time.perf_counter()
            res_puzzle = test_function(curr_puzzle)
            post = time.perf_counter()
            solve_time = post - pre
            print(f"Solved - {solve_time:.3f} seconds.")
            print("Puzzle:")
            print(res_puzzle)
            print()
