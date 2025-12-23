from tabulate import tabulate
from csv import writer

from itertools import groupby
from preprocessor import NoPreprocessor


def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)


class Summarizer:
    def __init__(self, summary_csv_file=None):
        self.summary_csv_file = summary_csv_file
        self.csv_writer = None
        self.csv_file = None
        if summary_csv_file:
            try:
                self.csv_file = open(summary_csv_file, "w", newline="")
                self.csv_writer = writer(self.csv_file)
            except Exception as e:
                print(f"Warning: Could not open summary CSV file '{summary_csv_file}': {e}")

    def groupby_solver_preprocessor(self, results):
        results.sort(key=lambda x: (x["solver_name"], x["preprocessor_name"]))
        return groupby(
            results, key=lambda x: (x["solver_name"], x["preprocessor_name"])
        )

    def groupby_dimacs(self, results):
        results.sort(key=lambda x: x["dimacs"])
        return groupby(results, key=lambda x: x["dimacs"])

    def groupby_solver(self, results):
        results.sort(key=lambda x: x["solver_name"])
        return groupby(results, key=lambda x: x["solver_name"])

    def run(self, results):
        successful_runs = list(filter(lambda x: x["finished"], results))

        # Compare the results of all solvers (without preprocessor)
        # and issue a warning if the disagree.
        for (dimacs, data) in self.groupby_dimacs(successful_runs):
            no_preprocessor_runs = filter(
                lambda x: x["preprocessor_name"] == NoPreprocessor.name, data
            )
            no_preprocessor_results = map(
                lambda x: x["number_of_solutions"], no_preprocessor_runs
            )
            if not all_equal(no_preprocessor_results):
                print(
                    "Not all solvers returned the same number of solutions for {}".format(
                        dimacs
                    )
                )

        # Compare the results of each solver (without preprocessor) to the result
        # of the same solver with each preprocessor and issue warnings if they disagree.
        reports = []
        for (dimacs, data) in self.groupby_dimacs(successful_runs):
            data = list(data)
            for (solver, runs) in self.groupby_solver(data):
                runs = list(runs)
                no_preprocessor_runs = list(
                    filter(
                        lambda x: x["preprocessor_name"] == NoPreprocessor.name, runs
                    )
                )
                if len(no_preprocessor_runs) > 0:
                    no_preprocessor_number_of_solutions = no_preprocessor_runs[0][
                        "number_of_solutions"
                    ]
                    preprocessor_runs = filter(
                        lambda x: x["preprocessor_name"] != NoPreprocessor.name, runs
                    )
                    for preprocessor_run in preprocessor_runs:
                        if (
                            preprocessor_run["factor_times_number"] is not None
                            and preprocessor_run["factor_times_number"]
                            != no_preprocessor_number_of_solutions
                        ):
                            reports.append(
                                (solver, preprocessor_run["preprocessor_name"], dimacs)
                            )

        # Remove duplicates
        reports = list(set(reports))
        for report in reports:
            print(
                "Solver {} returns a different number of solutions with preprocessor {} for {}".format(
                    report[0], report[1], report[2]
                )
            )

        # Print the summarized data
        print("Results:")
        table = []
        no_preprocessor_results = {}

        for ((solver, preprocessor), data) in self.groupby_solver_preprocessor(results):
            data = list(data)
            finished_data = list(filter(lambda x: x["finished"], data))
            if len(finished_data) > 0:
                avg_time_preprocessor = sum(
                    map(lambda x: x["preprocessor_time"], finished_data)
                ) / len(finished_data)
                avg_time_solver = sum(
                    map(lambda x: x["solver_time"], finished_data)
                ) / len(finished_data)
                avg_time_total = avg_time_preprocessor + avg_time_solver
                if preprocessor == NoPreprocessor().name:
                    no_preprocessor_results[solver] = avg_time_total
            else:
                avg_time_preprocessor = "No run finished"
                avg_time_solver = "No run finished"
                avg_time_total = "No run finished"

            percentage_finished = len(finished_data) * 100 / len(data)
            table.append(
                [
                    solver,
                    preprocessor,
                    avg_time_preprocessor,
                    avg_time_solver,
                    avg_time_total,
                    0.0,
                    percentage_finished,
                ]
            )

        for i in range(len(table)):
            if no_preprocessor_results.get(table[i][0]) and type(table[i][4]) == float:
                table[i][5] = no_preprocessor_results[table[i][0]] / table[i][4]
            else:
                table[i][5] = "No data"

        table.sort(key=lambda x: str(x[4]))

        headers = [
            "Solver",
            "Preprocessor",
            "Avg. preprocessor time",
            "Avg. solver time",
            "Avg. total time",
            "Avg. speedup",
            "Percentage finished",
        ]

        print(
            tabulate(
                table,
                headers=headers,
            )
        )

        # Write summary to CSV if requested
        if self.csv_writer:
            self.csv_writer.writerow(headers)
            for row in table:
                self.csv_writer.writerow(row)
            self.csv_file.close()
