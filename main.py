from argparse import ArgumentParser
from os.path import isfile

from progress.bar import Bar

from solver import ExecutableSolver
from preprocessor import ExecutablePreprocessor, NoPreprocessor, PreprocessorSequence
from benchmarker import Benchmarker
from summarizer import Summarizer
from writer import ResultWriter


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
    )


if __name__ == "__main__":
    main = ArgumentParser()

    subparsers = main.add_subparsers(dest="command")
    list_solvers = subparsers.add_parser("solvers")
    list_preprocessors = subparsers.add_parser("preprocessors")

    run = subparsers.add_parser("run")
    run.add_argument("-n", "--number-of-executions", default=1, type=int)
    run.add_argument("-p", "--preprocessor", nargs="+", default=[])
    run.add_argument("-t", "--timeout", type=float)
    run.add_argument("-s", "--solver", nargs="+", required=True)
    run.add_argument("-d", "--dimacs", nargs="+", required=True)
    run.add_argument("-o", "--output")

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
        ) = validate_arguments(args)

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
        )
        benchmarker.run()
