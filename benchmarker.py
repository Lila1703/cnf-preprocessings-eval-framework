from time import time
from os import remove, path
import sys
from util import get_comments_string, preprend_content, get_temp_dimacs_path, fix_pcnf_header_to_original

# Increase the limit for integer string conversion to handle very large solution counts
sys.set_int_max_str_digits(0)  # 0 means unlimited (Python 3.11+)


class Benchmarker:
    def __init__(
        self,
        preprocessors,
        solvers,
        dimacs,
        number_of_executions,
        timeout=None,
        mem_limit_mb=None,
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
        self.mem_limit_mb = mem_limit_mb
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

        if self.writer:
            self.writer.fieldnames = [
                "dimacs",
                "preprocessor_name",
                "solver_name",
                "preprocessor_time",
                "solver_time",
                "total_time",
                "preprocessing_factor",
                "number_of_solutions",
                "solutions_preserved",
            ]
            self.writer.writeheader()

        results = []

        for _ in range(self.number_of_executions):
            for dimacs in self.dimacs:
                # Ensure NoPreprocessor runs first so we can stream results
                # with solutions_preserved computed immediately.
                no_pre = [p for p in self.preprocessors if p.name == "NoPreprocessor"]
                others = [p for p in self.preprocessors if p.name != "NoPreprocessor"]
                ordered_preprocessors = no_pre + others

                original_counts = {}

                for preprocessor in ordered_preprocessors:
                    for solver in self.solvers:
                        solver_name = solver.name
                        preprocessor_name = preprocessor.name
                        target_path = get_temp_dimacs_path(
                            dimacs, preprocessor.name, self.keep_dimacs)

                        preprocessor_start_time = time()
                        # run method returns a factor to multiply the number of solutions with
                        preprocessing_factor = preprocessor.run(
                            dimacs, target_path, self.timeout)
                        preprocessor_time = time() - preprocessor_start_time

                        dimacs_comments = get_comments_string(dimacs)
                        # If preprocessing produced a target file, prepend original comments.
                        # Some preprocessors may time out and not write `target_path`.
                        if path.isfile(target_path):
                            preprend_content(dimacs_comments, target_path)
                            # Ensure the p cnf header uses the original variable count
                            # NOTE: Do NOT call this for SharpSatPreprocessor (or sequences containing it)
                            # as it eliminates unused variables and the header must reflect the actual var count
                            if "SharpSatPreprocessor" not in preprocessor_name:
                                try:
                                    fix_pcnf_header_to_original(dimacs, target_path)
                                except Exception:
                                    pass

                        solver_start_time = time()
                        # Use the preprocessed file if it exists, otherwise use an empty file
                        empty_file_path = None
                        if path.isfile(target_path):
                            solver_input_path = target_path
                        else:
                            # Create an empty file to indicate preprocessing failure
                            from uuid import uuid4
                            empty_file_path = get_temp_dimacs_path(dimacs, preprocessor.name + "_empty_" + uuid4().hex, self.keep_dimacs)
                            open(empty_file_path, 'w').close()
                            solver_input_path = empty_file_path
                        
                        try:
                            number_of_solutions_raw = solver.run(
                                solver_input_path,
                                self.timeout - preprocessor_time
                                if self.timeout is not None
                                else None,
                                mem_limit_mb=self.mem_limit_mb,
                            )
                            number_of_solutions = int(int(number_of_solutions_raw) * preprocessing_factor) if number_of_solutions_raw is not None and preprocessing_factor is not None else None
                        finally:
                            # Clean up empty file after solver finishes, but keep target_path
                            if empty_file_path and path.isfile(empty_file_path):
                                remove(empty_file_path)
                        
                        solver_time = time() - solver_start_time
                        
                        # Clean up preprocessed file after this solver is done
                        if not self.keep_dimacs and path.isfile(target_path):
                            remove(target_path)

                        if preprocessor_name == "NoPreprocessor" and number_of_solutions is not None:
                            original_counts[solver_name] = number_of_solutions

                        if preprocessor_name == "NoPreprocessor":
                            solutions_preserved = (
                                True if number_of_solutions is not None else None
                            )
                        elif original_counts.get(solver_name) is None or number_of_solutions is None:
                            solutions_preserved = None
                        else:
                            solutions_preserved = (
                                original_counts[solver_name] == number_of_solutions
                            )

                        entry = {
                            "solver_name": solver_name,
                            "preprocessor_name": preprocessor_name,
                            "dimacs": dimacs,
                            "preprocessor_time": preprocessor_time,
                            "solver_time": solver_time,
                            "total_time": preprocessor_time + solver_time,
                            "preprocessing_factor": preprocessing_factor,
                            "number_of_solutions": number_of_solutions,
                            "finished": number_of_solutions is not None,
                            "solutions_preserved": solutions_preserved,
                        }

                        results.append(entry)
                        if self.writer:
                            self.writer.writerows([entry])

                        if self.progress_bar:
                            self.progress_bar.next()

        if self.progress_bar:
            self.progress_bar.finish()
            print()

        if self.summarizer:
            self.summarizer.run(results)

        if self.writer:
            self.writer.flush()
