from argparse import ArgumentParser
from os.path import isfile

from progress.bar import Bar

from solver import ExecutableSolver
from preprocessor import ExecutablePreprocessor, NoPreprocessor, PreprocessorSequence
from benchmarker import Benchmarker
from summarizer import Summarizer
from equivalence_checker import EquivalenceChecker
from equivalence_summarizer import EquivalenceSummarizer
from writer import ResultWriter
from util import get_temp_dimacs_path, get_comments_string, preprend_content
import os
from equivalence_check import build_diff_cnf, run_sat_solver


def find_subclass_by_name(name, classes):
    for cls in classes:
        if cls.__name__.lower() == name.lower():
            return cls


def find_solver_by_name(name):
    return find_subclass_by_name(name, ExecutableSolver.__subclasses__())


def find_preprocessor_by_name(name):
    return find_subclass_by_name(name, ExecutablePreprocessor.__subclasses__())


def find_preprocessors_by_names(names):
    names = names.split()
    preprocessors = []
    for name in names:
        preprocessor = find_preprocessor_by_name(name)
        if preprocessor:
            preprocessors.append(preprocessor())
        else:
            return None
    if len(preprocessors) > 1:
        return PreprocessorSequence(preprocessors)
    elif len(preprocessors) == 1:
        return preprocessors[0]


def names_of_subclasses(cls):
    return [scls.__name__ for scls in cls.__subclasses__()]


def expand_dimacs_paths(paths):
    """Expand paths to include files from directories recursively."""
    expanded = []
    for path in paths:
        if os.path.isfile(path):
            expanded.append(path)
        elif os.path.isdir(path):
            # Recursively find all files in the directory
            for root, dirs, files in os.walk(path):
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    expanded.append(file_path)
        else:
            print("Path '{}' doesn't exist".format(path))
            exit(1)
    return expanded


def validate_arguments(args):
    solvers = []
    preprocessors = []

    for p in args.preprocessor:
        preprocessor = find_preprocessors_by_names(p)
        if preprocessor is None:
            print("Preprocessor '{}' is not registered".format(p))
            exit(1)
        preprocessors.append(preprocessor)

    if not args.nonopreprocessor:
        preprocessors.append(NoPreprocessor())

    for s in args.solver:
        solver = find_solver_by_name(s)
        if solver is None:
            print("Solver '{}' is not registered".format(s))
            exit(1)
        solvers.append(solver())

    # Expand paths: if directory, recursively find all files inside
    dimacs = expand_dimacs_paths(args.dimacs)
    
    if not dimacs:
        print("No DIMACS files found in the provided paths")
        exit(1)

    if args.number_of_executions < 1:
        print(
            "Number of executions {} cannot be smaller than one".format(
                args.number_of_executions
            )
        )
        exit(1)

    if args.timeout and args.timeout <= 0:
        print("Timeout {} must be greater than zero".format(args.timeout))
        exit(1)

    if args.keep_dimacs:
        keep_dimacs = True
    else:
        keep_dimacs = False

    if args.copy_comments:
        copy_comments = True
    else:
        copy_comments = False

    if args.output:
        file = open(args.output, "w", newline="")
        writer = ResultWriter(file, [])
    else:
        writer = None

    return (
        solvers,
        preprocessors,
        dimacs,
        args.number_of_executions,
        args.timeout,
        getattr(args, "mem_limit_mb", None),
        writer,
        keep_dimacs,
        copy_comments
    )


if __name__ == "__main__":
    main = ArgumentParser()

    subparsers = main.add_subparsers(dest="command")
    list_solvers = subparsers.add_parser("solvers")
    list_preprocessors = subparsers.add_parser("preprocessors")

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("input", help="Path to input CSV file (e.g., output.csv)")
    summarize.add_argument("-o", "--output", help="Path to output summary CSV file (default: <input>_summary.csv)")

    run = subparsers.add_parser("run")
    run.add_argument("-n", "--number-of-executions", default=1, type=int)
    run.add_argument("-a", "--accumulate", action="store_true", help="Run each preprocessor repeated 1..n times (accumulate)")
    run.add_argument("-p", "--preprocessor", nargs="+", default=[])
    run.add_argument("-t", "--timeout", type=float)
    run.add_argument("--mem-limit-mb", type=int, help="Per-process memory limit in MB (applies to solvers)")
    run.add_argument("-s", "--solver", nargs="+", required=True)
    run.add_argument("-d", "--dimacs", nargs="+", required=True)
    run.add_argument("-o", "--output")
    run.add_argument("-sum", "--summary", help="Path to output summary CSV file (default: summary.csv)", nargs="?", const="summary.csv")
    run.add_argument("-k", "--keep_dimacs", action="store_true", dest="keep_dimacs")
    run.add_argument("-c", "--copy_comments", action="store_true", dest="copy_comments")
    run.add_argument("--nonopreprocessor", action="store_true", help="Disable automatic execution of NoPreprocessor baseline")

    check = subparsers.add_parser("check")
    check.add_argument("-p", "--preprocessor", nargs="+", default=[])
    check.add_argument("-t", "--timeout", type=float)
    check.add_argument("--mem-limit-mb", type=int, help="Per-process memory limit in MB (applies to counter solver)")
    check.add_argument("-d", "--dimacs", nargs="+", required=True)
    check.add_argument("-S", "--sat-solver", default="./solvers/MiniSat_v1.14_linux {input}")
    check.add_argument("--counter", default="d4", help="Name of counting solver class to use (e.g. D4V2, SharpSat)")
    check.add_argument("-o", "--output")
    check.add_argument("-sum", "--summary", help="Path to output summary CSV file (default: equivalence_summary.csv)", nargs="?", const="equivalence_summary.csv")
    check.add_argument("-k", "--keep_dimacs", action="store_true", dest="keep_dimacs")
    check.add_argument("-c", "--copy_comments", action="store_true", dest="copy_comments")

    args = main.parse_args()
    if args.command == "solvers":
        print("The following solvers are registered:")
        print("\n".join(names_of_subclasses(ExecutableSolver)))

    if args.command == "preprocessors":
        print("The following preprocessors are registered:")
        print("\n".join(names_of_subclasses(ExecutablePreprocessor)))

    if args.command == "summarize":
        input_file = args.input
        
        if not os.path.isfile(input_file):
            print(f"Error: Input file '{input_file}' not found")
            exit(1)
        
        # Determine output file name
        if args.output:
            output_file = args.output
        else:
            # Generate default output name: output.csv -> output_summary.csv
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_summary.csv"
        
        summarizer = Summarizer(summary_csv_file=output_file)
        summarizer.summarize(input_file)

    if args.command == "run":

        (
            solvers,
            preprocessors,
            dimacs,
            number_of_executions,
            timeout,
            mem_limit_mb,
            output_writer,
            keep_dimacs,
            copy_comments,
        ) = validate_arguments(args)

        # If accumulate is requested, expand each preprocessor into sequences
        # applied 1..n times. Keep NoPreprocessor as a single baseline entry.
        if getattr(args, "accumulate", False):
            expanded = []
            max_k = args.number_of_executions
            for pre in preprocessors:
                # Don't expand the NoPreprocessor baseline
                if isinstance(pre, NoPreprocessor):
                    expanded.append(pre)
                    continue

                # Determine base sequence (single preprocessor or existing sequence)
                if isinstance(pre, PreprocessorSequence):
                    base = pre.preprocessors
                else:
                    base = [pre]

                for k in range(1, max_k + 1):
                    seq = []
                    for _ in range(k):
                        seq.extend(base)
                    expanded.append(PreprocessorSequence(seq))

            preprocessors = expanded
            # After expansion, we don't want to repeat the whole benchmark multiple times
            number_of_executions = 1

        progress_bar = Bar(
            "Benchmarking", width=50, suffix="%(index)d/%(max)d - ETA: %(eta)ds"
        )

        summarizer = Summarizer(summary_csv_file=args.summary)

        benchmarker = Benchmarker(
            preprocessors,
            solvers,
            dimacs,
            number_of_executions,
            timeout,
            mem_limit_mb,
            summarizer,
            output_writer,
            progress_bar,
            keep_dimacs,
            copy_comments
        )
        benchmarker.run()

    if args.command == "check":

        # validate preprocessors
        preprocessors = []
        for p in args.preprocessor:
            preprocessor = find_preprocessors_by_names(p)
            if preprocessor is None:
                print("Preprocessor '{}' is not registered".format(p))
                exit(1)
            preprocessors.append(preprocessor)

        # Do not add NoPreprocessor here — comparing the original to itself is pointless.
        if not preprocessors:
            print("No preprocessors specified; nothing to check. Use -p to list preprocessors.")
            exit(0)

        # Expand paths: if directory, recursively find all files inside
        dimacs_files = expand_dimacs_paths(args.dimacs)
        
        if not dimacs_files:
            print("No DIMACS files found in the provided paths")
            exit(1)

        if args.timeout and args.timeout <= 0:
            print("Timeout {} must be greater than zero".format(args.timeout))
            exit(1)

        keep_dimacs = True if args.keep_dimacs else False
        copy_comments = True if args.copy_comments else False

        sat_solver = args.sat_solver
        counter_name = args.counter
        
        # If default MiniSat binary is present but not executable, try to fix permissions
        try:
            solver_first_token = sat_solver.split()[0]
            if solver_first_token.startswith('./solvers'):
                solver_path = solver_first_token
                if os.path.exists(solver_path):
                    if not os.access(solver_path, os.X_OK):
                        try:
                            os.chmod(solver_path, 0o755)
                            print(f"Made solver executable: {solver_path}")
                        except Exception:
                            print(f"Solver found but could not make executable: {solver_path}")
                else:
                    print(f"Warning: solver binary not found at {solver_path}. Please place your solver binary there or pass -S with the correct path.")
        except Exception:
            pass

        # Get counter solver instance
        counter_cls = find_solver_by_name(counter_name)
        if counter_cls is None:
            print(f"Counter solver '{counter_name}' is not registered. Available solvers: {', '.join(names_of_subclasses(ExecutableSolver))}")
            exit(1)
        counter = counter_cls()

        # Setup output writer if requested
        if args.output:
            file = open(args.output, "w", newline="")
            output_writer = ResultWriter(file, [])
        else:
            output_writer = None

        # Setup progress bar
        progress_bar = Bar(
            "Checking", width=50, suffix="%(index)d/%(max)d - ETA: %(eta)ds"
        )

        # Setup summarizer
        summarizer = EquivalenceSummarizer(summary_csv_file=args.summary)

        # Create and run equivalence checker
        checker = EquivalenceChecker(
            preprocessors,
            dimacs_files,
            counter,
            sat_solver,
            args.timeout,
            getattr(args, "mem_limit_mb", None),
            summarizer,
            output_writer,
            progress_bar,
            keep_dimacs,
            copy_comments
        )
        checker.run()
