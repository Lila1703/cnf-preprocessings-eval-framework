from tabulate import tabulate
from csv import writer, DictReader

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

    def summarize(self, input_csv_file):
        """Read results from a CSV file and generate a summary."""
        results = []
        
        try:
            with open(input_csv_file, "r") as f:
                reader = DictReader(f)
                for row in reader:
                    # Convert string values to appropriate types
                    result = {
                        "dimacs": row["dimacs"],
                        "preprocessor_name": row["preprocessor_name"],
                        "solver_name": row["solver_name"],
                        "preprocessor_time": float(row["preprocessor_time"]) if row["preprocessor_time"] else 0.0,
                        "solver_time": float(row["solver_time"]) if row["solver_time"] else 0.0,
                        "number_of_solutions": row["number_of_solutions"] if row["number_of_solutions"] else None,
                        "solutions_preserved": row.get("solutions_preserved", "unknown"),
                        "finished": True if row["number_of_solutions"] else None,
                    }
                    results.append(result)
        except FileNotFoundError:
            print(f"Error: Input file '{input_csv_file}' not found")
            return
        except Exception as e:
            print(f"Error reading input file '{input_csv_file}': {e}")
            return
        
        if not results:
            print("No results found in input file")
            return
        
        # Use the same logic as run() method
        self.run(results)

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
                    no_preprocessor_number_of_solutions = no_preprocessor_runs[0]["number_of_solutions"]
                    preprocessor_runs = filter(
                        lambda x: x["preprocessor_name"] != NoPreprocessor.name, runs
                    )
                    for preprocessor_run in preprocessor_runs:
                        if (
                            preprocessor_run["number_of_solutions"] is not None
                            and no_preprocessor_number_of_solutions is not None
                            and preprocessor_run["number_of_solutions"]
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
        # Track which DIMACS files were successfully completed by NoPreprocessor for each solver
        no_preprocessor_successful_dimacs = {}

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
                    # Track which DIMACS files were successfully completed by NoPreprocessor
                    no_preprocessor_successful_dimacs[solver] = set(
                        x["dimacs"] for x in finished_data
                    )
                
                # Determine solutions_preserved status
                # Desired behavior:
                # - "yes"  if all entries are either "yes" or "unknown"
                # - "no"   if all entries are either "no" or "unknown"
                # - "partly" otherwise
                # Note: treat None/empty/unrecognized values as "unknown" and compare case-insensitively.
                # Base classification on all runs for this solver+preprocessor,
                # not only finished ones, as requested.
                raw_values = [x.get("solutions_preserved") for x in data]
                normalized = []
                for v in raw_values:
                    if v is None:
                        nv = "unknown"
                    elif isinstance(v, bool):
                        nv = "yes" if v else "no"
                    else:
                        nv = str(v).strip().lower()
                        if nv not in ("yes", "no", "unknown"):
                            nv = "unknown"
                    normalized.append(nv)

                if all(v in ("yes", "unknown") for v in normalized):
                    solutions_preserved = "yes"
                elif all(v in ("no", "unknown") for v in normalized):
                    solutions_preserved = "no"
                else:
                    solutions_preserved = "partly"

            else:
                avg_time_preprocessor = "No run finished"
                avg_time_solver = "No run finished"
                avg_time_total = "No run finished"
                solutions_preserved = "No run finished"

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
                    solutions_preserved,
                ]
            )

        for i in range(len(table)):
            solver = table[i][0]
            preprocessor = table[i][1]
            current_time = table[i][4]
            table[i][5] = "No data"  # Default value
            
            # Calculate speedup based only on DIMACS files that NoPreprocessor completed
            if (solver in no_preprocessor_results and 
                solver in no_preprocessor_successful_dimacs and
                preprocessor != NoPreprocessor().name and
                type(current_time) == float):
                
                # Find the runs for this solver+preprocessor combination
                matching_runs = [
                    x for x in results 
                    if x["solver_name"] == solver 
                    and x["preprocessor_name"] == preprocessor
                    and x["finished"]
                    and x["dimacs"] in no_preprocessor_successful_dimacs[solver]
                ]
                
                if matching_runs:
                    # Calculate average time for only the DIMACS files that NoPreprocessor completed
                    average_time_total_speedup = sum(
                        x["preprocessor_time"] + x["solver_time"] 
                        for x in matching_runs
                    ) / len(matching_runs)
                    table[i][5] = no_preprocessor_results[solver] / average_time_total_speedup

        table.sort(key=lambda x: str(x[4]))

        headers = [
            "Solver",
            "Preprocessor",
            "Avg. preprocessor time",
            "Avg. solver time",
            "Avg. total time",
            "Avg. speedup",
            "Percentage finished",
            "Solutions preserved",
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
