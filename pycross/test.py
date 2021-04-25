"""
Script in order to run tests on the project files.
"""
import sys
import os
import argparse
import functools
import time
from multiprocessing import Process, Queue

import pycross
import astar
import backtrack

TIMEOUT = 120


def run_test(puzzle, solver_function, send_queue):
    res_puzzle = solver_function(puzzle)
    send_queue.put(res_puzzle)


if __name__ == '__main__':

    res_queue = Queue()

    parser = argparse.ArgumentParser(description="Run test cases on the algorithms made for the project.")
    parser.add_argument('-a', '--algorithm', choices=["astar", "csp"], required=True, help="which algorithm(s) to run")
    parser.add_argument('-t', '--testcase', required=True, help="which testcase(s) to run")

    args = parser.parse_args()

    # Do extra things to select algorithm here
    test_function = functools.partial(astar.perform_search, cost_function=astar.cost_mul_function)
    if args.algorithm == "csp":
        test_function = backtrack.constraint_search

    print(f"Selected algorithm: {args.algorithm}")

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

                test_process = Process(target=run_test, args=(curr_puzzle, test_function, res_queue))

                pre = time.perf_counter()
                test_process.start()
                test_process.join(TIMEOUT)
                post = time.perf_counter()
                solve_time = post - pre
                if test_process.is_alive():
                    print(f"Timeout - Not solved after {TIMEOUT} seconds.")
                    print()
                else:
                    result = res_queue.get()
                    print(f"Solved - {solve_time:.3f} seconds.")
                    print("Puzzle:")
                    print(result)
