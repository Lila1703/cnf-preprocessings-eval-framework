from argparse import ArgumentParser, BooleanOptionalAction
from os.path import isfile

from progress.bar import Bar

from solver import ExecutableSolver
from preprocessor import ExecutablePreprocessor, NoPreprocessor, PreprocessorSequence
from benchmarker import Benchmarker
from summarizer import Summarizer
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


def validate_arguments(args):
    solvers = []
    preprocessors = []

    for p in args.preprocessor:
        preprocessor = find_preprocessors_by_names(p)
        if preprocessor is None:
            print("Preprocessor '{}' is not registered".format(p))
            exit(1)
        preprocessors.append(preprocessor)

    preprocessors.append(NoPreprocessor())

    for s in args.solver:
        solver = find_solver_by_name(s)
        if solver is None:
            print("Solver '{}' is not registered".format(s))
            exit(1)
        solvers.append(solver())

    for d in args.dimacs:
        if not isfile(d):
            print("File '{}' doesn't exist".format(d))
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
        args.dimacs,
        args.number_of_executions,
        args.timeout,
        writer,
        keep_dimacs,
        copy_comments
    )


if __name__ == "__main__":
    main = ArgumentParser()

    subparsers = main.add_subparsers(dest="command")
    list_solvers = subparsers.add_parser("solvers")
    list_preprocessors = subparsers.add_parser("preprocessors")

    run = subparsers.add_parser("run")
    run.add_argument("-n", "--number-of-executions", default=1, type=int)
    run.add_argument("-a", "--accumulate", action="store_true", help="Run each preprocessor repeated 1..n times (accumulate)")
    run.add_argument("-p", "--preprocessor", nargs="+", default=[])
    run.add_argument("-t", "--timeout", type=float)
    run.add_argument("-s", "--solver", nargs="+", required=True)
    run.add_argument("-d", "--dimacs", nargs="+", required=True)
    run.add_argument("-o", "--output")
    run.add_argument("-k", "--keep_dimacs", action=BooleanOptionalAction)
    run.add_argument("-c", "--copy_comments", action=BooleanOptionalAction)

    check = subparsers.add_parser("check")
    check.add_argument("-p", "--preprocessor", nargs="+", default=[])
    check.add_argument("-t", "--timeout", type=float)
    check.add_argument("-d", "--dimacs", nargs="+", required=True)
    check.add_argument("-S", "--sat-solver", default="./solvers/MiniSat_v1.14_linux {input}")
    check.add_argument("--count-check", action="store_true", help="Run a model-count check instead of the SAT equivalence check")
    check.add_argument("--counter", default="SharpSat", help="Name of counting solver class to use (e.g. D4V2, SharpSat)")
    check.add_argument("-k", "--keep_dimacs", action=BooleanOptionalAction)
    check.add_argument("-c", "--copy_comments", action=BooleanOptionalAction)

    args = main.parse_args()
    if args.command == "solvers":
        print("The following solvers are registered:")
        print("\n".join(names_of_subclasses(ExecutableSolver)))

    if args.command == "preprocessors":
        print("The following preprocessors are registered:")
        print("\n".join(names_of_subclasses(ExecutablePreprocessor)))

    if args.command == "run":

        (
            solvers,
            preprocessors,
            dimacs,
            number_of_executions,
            timeout,
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

        summarizer = Summarizer()

        benchmarker = Benchmarker(
            preprocessors,
            solvers,
            dimacs,
            number_of_executions,
            timeout,
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

        for d in args.dimacs:
            if not isfile(d):
                print("File '{}' doesn't exist".format(d))
                exit(1)

        if args.timeout and args.timeout <= 0:
            print("Timeout {} must be greater than zero".format(args.timeout))
            exit(1)

        keep_dimacs = True if args.keep_dimacs else False
        copy_comments = True if args.copy_comments else False

        sat_solver = args.sat_solver
        do_count_check = args.count_check
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

        # For each dimacs and preprocessor produce a PASS/FAIL
        for dimacs in args.dimacs:
            for preprocessor in preprocessors:
                preprocessor_name = preprocessor.name
                target_path = get_temp_dimacs_path(dimacs, preprocessor.name, keep_dimacs)

                # run preprocessor
                factor = preprocessor.run(dimacs, target_path, args.timeout)

                if copy_comments:
                    comments = get_comments_string(dimacs)
                    preprend_content(comments, target_path)

                # If requested, run a counting-based check: compare model counts
                if do_count_check:
                    counter_cls = find_solver_by_name(counter_name)
                    if counter_cls is None:
                        print(f"Counter solver '{counter_name}' is not registered. Available solvers: {', '.join(names_of_subclasses(ExecutableSolver))}")
                        if not keep_dimacs and os.path.exists(target_path):
                            try:
                                os.remove(target_path)
                            except Exception:
                                pass
                        exit(1)

                    counter = counter_cls()
                    orig_count = counter.run(dimacs, args.timeout)
                    pre_count = counter.run(target_path, args.timeout)

                    status = 'UNKNOWN'
                    try:
                        from fractions import Fraction

                        if orig_count is None or pre_count is None:
                            status = 'UNKNOWN'
                        elif factor is None:
                            status = 'PASS' if orig_count == pre_count else 'FAIL'
                        else:
                            expected = Fraction(pre_count) * Fraction(factor)
                            if expected.denominator == 1:
                                status = 'PASS' if orig_count == expected.numerator else 'FAIL'
                            else:
                                status = 'FAIL'
                    except Exception:
                        status = 'UNKNOWN'

                    if not keep_dimacs and os.path.exists(target_path):
                        try:
                            os.remove(target_path)
                        except Exception:
                            pass

                    print(f"{preprocessor_name} on {dimacs}: {status} (count-check using {counter_name})")
                    continue

                # build difference CNFs and run SAT checks
                base = os.path.splitext(os.path.basename(dimacs))[0]
                check1 = f"temp.check.{preprocessor_name}.{base}.1.dimacs"
                check2 = f"temp.check.{preprocessor_name}.{base}.2.dimacs"

                build_diff_cnf(dimacs, target_path, check1, mode='F_and_not_G')
                sat1 = run_sat_solver(sat_solver, check1, timeout=args.timeout)

                build_diff_cnf(dimacs, target_path, check2, mode='G_and_not_F')
                sat2 = run_sat_solver(sat_solver, check2, timeout=args.timeout)

                # cleanup
                if not keep_dimacs and os.path.exists(target_path):
                    try:
                        os.remove(target_path)
                    except Exception:
                        pass
                for f in (check1, check2):
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                        except Exception:
                            pass

                status = None
                if sat1 is None or sat2 is None:
                    status = 'UNKNOWN'
                elif sat1 or sat2:
                    status = 'FAIL'
                else:
                    status = 'PASS'

                print(f"{preprocessor_name} on {dimacs}: {status}")
