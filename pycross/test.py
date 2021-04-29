"""
Script in order to run tests on the project files.
"""
import os
import argparse
import functools
import time
from datetime import datetime
from multiprocessing import Process, Queue

import pycross
import search
import backtrack
import q_learning_agent

TIMEOUT = 180  # The time in seconds after which a test is terminated.


def run_test(puzzle, solver_function, send_queue):
    pre = time.perf_counter()
    res_puzzle = solver_function(puzzle)
    post = time.perf_counter()
    solve_time = post - pre
    send_queue.put((solve_time, res_puzzle))


if __name__ == '__main__':

    res_queue = Queue()

    parser = argparse.ArgumentParser(description="Run test cases on the algorithms made for the project.")
    parser.add_argument('-a', '--algorithm', choices=["search", "csp", "q-learning"], required=True, help="which algorithm(s) to run")
    parser.add_argument('-t', '--testcase', required=True, help="which testcase(s) to run")
    parser.add_argument('-l', '--log', default=False, action="store_true", help="output test results to log file")
    parser.add_argument('-c', '--compact', default=True, action="store_true",
                        help="reduce size of log, not print puzzle")

    args = parser.parse_args()

    # Do extra things to select algorithm here
    # Default to search so that the IDE shuts up
    test_function = functools.partial(search.perform_search, cost_function=search.cost_mul_function)
    if args.algorithm == "csp":
        test_function = backtrack.constraint_search
    if args.algorithm == "q-learning":
        test_function = q_learning_agent.solve

    print(f"Selected algorithm: {args.algorithm}")

    # if outputting to logfile, open file locally
    logfile = None
    if args.log:
        logfile = open(f"testlog_{datetime.now().strftime('%Y-%m-%dT%H_%M_%S')}.txt", "w")
        print(f"Selected algorithm: {args.algorithm}", file=logfile)

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
            if args.log:
                print(f"Running {test_set}:", file=logfile)
            for case in test_cases:
                if not args.compact:
                    print(f"Loading {case}...")
                    if args.log:
                        print(f"Loading {case}...", file=logfile)
                # Import the puzzle (probably want to do error checks on this)
                curr_puzzle = pycross.from_json(open(case).read())
                if not args.compact:
                    print(f"Beginning test on {case}...")
                    if args.log:
                        print(f"Beginning test on {case}...", file=logfile)
                # Start solving!

                test_process = Process(target=run_test, args=(curr_puzzle, test_function, res_queue))

                test_process.start()
                test_process.join(TIMEOUT)
                if test_process.is_alive():
                    test_process.terminate()
                    test_process.join()
                    if args.compact:
                        print(f"{case} - Timeout after {TIMEOUT} seconds.")
                        if args.log:
                            print(f"{case} - Timeout after {TIMEOUT} seconds.", file=logfile)
                    else:
                        print(f"Timeout - Not solved after {TIMEOUT} seconds.")
                        print()
                        if args.log:
                            print(f"Timeout - Not solved after {TIMEOUT} seconds.", file=logfile)
                            print("", file=logfile)
                else:
                    solve_time, result = res_queue.get()
                    if args.compact:
                        print(f"{case} - Solved after {solve_time:.4f} seconds.")
                        if args.log:
                            print(f"{case} - Solved after {solve_time:.4f} seconds.", file=logfile)
                    else:
                        print(f"Solved - {solve_time:.4f} seconds.")
                        print("Puzzle:")
                        print(result)
                        if args.log:
                            print(f"Solved - {solve_time:.4f} seconds.", file=logfile)
                            print("Puzzle:", file=logfile)
                            print(result, file=logfile)

    if logfile is not None:
        logfile.close()
