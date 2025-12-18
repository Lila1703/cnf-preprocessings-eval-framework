from time import time
from os import remove, path
from util import get_comments_string, preprend_content, get_temp_dimacs_path


class Benchmarker:
    def __init__(
        self,
        preprocessors,
        solvers,
        dimacs,
        number_of_executions,
        timeout=None,
        summarizer=None,
        writer=None,
        progress_bar=None,
        keep_dimacs=False,
        copy_comments=False
    ):
        self.preprocessors = preprocessors
        self.dimacs = dimacs
        self.solvers = solvers
        self.number_of_executions = number_of_executions
        self.timeout = timeout
        self.summarizer = summarizer
        self.writer = writer
        self.progress_bar = progress_bar
        self.keep_dimacs = keep_dimacs
        self.copy_comments = copy_comments

    def run(self):
        if self.progress_bar:
            self.progress_bar.max = (
                len(self.preprocessors)
                * len(self.solvers)
                * len(self.dimacs)
                * self.number_of_executions
            )

        results = []

        for _ in range(self.number_of_executions):
            for dimacs in self.dimacs:
                # Collect results for this dimacs+execution locally so we can
                # determine the original model counts from the NoPreprocessor run
                # regardless of its position in the preprocessor list.
                local_results = []

                for preprocessor in self.preprocessors:
                    for solver in self.solvers:
                        solver_name = solver.name
                        preprocessor_name = preprocessor.name
                        target_path = get_temp_dimacs_path(dimacs, preprocessor.name, self.keep_dimacs)

                        preprocessor_start_time = time()
                        factor = preprocessor.run(dimacs, target_path, self.timeout)
                        preprocessor_time = time() - preprocessor_start_time

                        dimacs_comments = get_comments_string(dimacs)
                        preprend_content(dimacs_comments, target_path)

                        solver_start_time = time()
                        number_of_solutions = solver.run(
                            target_path,
                            self.timeout - preprocessor_time
                            if self.timeout is not None
                            else None,
                        )
                        solver_time = time() - solver_start_time

                        if not self.keep_dimacs:
                            remove(target_path)

                        factor_times_number = (
                            factor * number_of_solutions
                            if factor is not None and number_of_solutions is not None
                            else None
                        )

                        entry = {
                            "solver_name": solver_name,
                            "preprocessor_name": preprocessor_name,
                            "dimacs": dimacs,
                            "preprocessor_time": preprocessor_time,
                            "solver_time": solver_time,
                            "total_time": preprocessor_time + solver_time,
                            "factor": factor,
                            "number_of_solutions": number_of_solutions,
                            "factor_times_number": factor_times_number,
                            "finished": number_of_solutions is not None,
                            # fill solutions_preserved later after we know NoPreprocessor
                            "solutions_preserved": None,
                        }

                        local_results.append(entry)

                        if self.progress_bar:
                            self.progress_bar.next()

                # Determine original counts from NoPreprocessor runs in local_results
                original_counts = {}
                for r in local_results:
                    if r["preprocessor_name"] == "NoPreprocessor":
                        original_counts[r["solver_name"]] = r["number_of_solutions"]

                # Update solutions_preserved for all local results
                for r in local_results:
                    orig = original_counts.get(r["solver_name"])
                    if orig is None or r["number_of_solutions"] is None:
                        r["solutions_preserved"] = None
                    else:
                        r["solutions_preserved"] = orig == r["number_of_solutions"]

                results.extend(local_results)

        if self.progress_bar:
            self.progress_bar.finish()
            print()

        if self.summarizer:
            self.summarizer.run(results)

        if self.writer:
            self.writer.fieldnames = [
                "solver_name",
                "preprocessor_name",
                "dimacs",
                "preprocessor_time",
                "solver_time",
                "total_time",
                "factor",
                "number_of_solutions",
                #"factor_times_number",
                "solutions_preserved",
            ]
            self.writer.writeheader()
            self.writer.writerows(results)
