from time import time
from os import remove, path


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
        keep_dimacs=False
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
                for preprocessor in self.preprocessors:
                    for solver in self.solvers:
                        solver_name = solver.name
                        preprocessor_name = preprocessor.name
                        target_path = "temp.dimacs" if not self.keep_dimacs else f'{preprocessor_name}-{path.basename(dimacs)}'

                        preprocessor_start_time = time()  
                        factor = preprocessor.run(dimacs, target_path, self.timeout)
                        preprocessor_time = time() - preprocessor_start_time

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

                        results.append(
                            {
                                "solver_name": solver_name,
                                "preprocessor_name": preprocessor_name,
                                "dimacs": dimacs,
                                "preprocessor_time": preprocessor_time,
                                "solver_time": solver_time,
                                "factor": factor,
                                "number_of_solutions": number_of_solutions,
                                "factor_times_number": factor_times_number,
                                "finished": number_of_solutions is not None,
                            }
                        )

                        if self.progress_bar:
                            self.progress_bar.next()

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
                "factor",
                "number_of_solutions",
                "factor_times_number",
                "finished",
            ]
            self.writer.writeheader()
            self.writer.writerows(results)
