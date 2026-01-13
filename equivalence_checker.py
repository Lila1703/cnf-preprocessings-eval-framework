from time import time
from os import remove, path
import os
from util import get_comments_string, preprend_content, get_temp_dimacs_path
from equivalence_check import build_diff_cnf, run_sat_solver
from fractions import Fraction


class EquivalenceChecker:
    def __init__(
        self,
        preprocessors,
        dimacs,
        counter_solver,
        sat_solver,
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
        self.counter_solver = counter_solver
        self.sat_solver = sat_solver
        self.timeout = timeout
        self.mem_limit_mb = mem_limit_mb
        self.summarizer = summarizer
        self.writer = writer
        self.progress_bar = progress_bar
        self.keep_dimacs = keep_dimacs
        self.copy_comments = copy_comments

    def run(self):
        if self.progress_bar:
            self.progress_bar.max = len(self.preprocessors) * len(self.dimacs)

        results = []

        for dimacs in self.dimacs:
            # Get original count once per dimacs file and normalize to int if possible
            original_count = None
            original_count_int = None
            if self.counter_solver:
                try:
                    original_count = self.counter_solver.run(
                        dimacs, self.timeout, mem_limit_mb=self.mem_limit_mb
                    )
                    if original_count is not None:
                        try:
                            original_count_int = int(original_count)
                        except (ValueError, TypeError):
                            original_count_int = None
                except Exception:
                    original_count = None
                    original_count_int = None

            for preprocessor in self.preprocessors:
                preprocessor_name = preprocessor.name
                target_path = get_temp_dimacs_path(
                    dimacs, preprocessor.name, self.keep_dimacs
                )

                # Run preprocessor
                preprocessor_start_time = time()
                factor = None
                try:
                    factor = preprocessor.run(dimacs, target_path, self.timeout)
                except Exception:
                    pass
                preprocessor_time = time() - preprocessor_start_time

                # If copy_comments is enabled, prepend comments
                if self.copy_comments and path.isfile(target_path):
                    comments = get_comments_string(dimacs)
                    preprend_content(comments, target_path)

                # Initialize result entry
                entry = {
                    "dimacs": dimacs,
                    "preprocessor_name": preprocessor_name,
                    "preprocessor_time": preprocessor_time,
                    "logically_equivalent": "unknown",
                    "count_check_status": "UNKNOWN",
                    "sat_check_status": "UNKNOWN",
                }

                # Run count check
                if self.counter_solver and path.isfile(target_path):
                    try:
                        pre_count = self.counter_solver.run(
                            target_path, self.timeout, mem_limit_mb=self.mem_limit_mb
                        )

                        # Convert counts to integers (solver.run() may return strings)
                        pre_count_int = None
                        if pre_count is not None:
                            try:
                                pre_count_int = int(pre_count)
                            except (ValueError, TypeError):
                                pass

                        if original_count_int is None or pre_count_int is None:
                            entry["count_check_status"] = "UNKNOWN"
                        elif factor is None:
                            # No factor returned, so we expect counts to be equal
                            if original_count_int == pre_count_int:
                                entry["count_check_status"] = "PASS"
                            else:
                                entry["count_check_status"] = "FAIL"
                        else:
                            # Factor was returned, compute expected original count
                            expected = Fraction(pre_count_int) * Fraction(factor)
                            if expected.denominator == 1:
                                if original_count_int == expected.numerator:
                                    entry["count_check_status"] = "PASS"
                                else:
                                    entry["count_check_status"] = "FAIL"
                            else:
                                entry["count_check_status"] = "FAIL"
                    except Exception:
                        entry["count_check_status"] = "ERROR"
                else:
                    entry["count_check_status"] = "SKIPPED"

                # Run SAT equivalence check
                if path.isfile(target_path):
                    try:
                        base = os.path.splitext(os.path.basename(dimacs))[0]
                        check1 = f"temp.check.{preprocessor_name}.{base}.1.dimacs"
                        check2 = f"temp.check.{preprocessor_name}.{base}.2.dimacs"

                        build_diff_cnf(dimacs, target_path, check1, mode="F_and_not_G")
                        sat1 = run_sat_solver(self.sat_solver, check1, timeout=self.timeout)

                        build_diff_cnf(dimacs, target_path, check2, mode="G_and_not_F")
                        sat2 = run_sat_solver(self.sat_solver, check2, timeout=self.timeout)

                        # Cleanup check files
                        for f in (check1, check2):
                            if os.path.exists(f):
                                try:
                                    os.remove(f)
                                except Exception:
                                    pass

                        if sat1 is None or sat2 is None:
                            entry["sat_check_status"] = "UNKNOWN"
                            entry["logically_equivalent"] = "unknown"
                        elif sat1 or sat2:
                            entry["sat_check_status"] = "FAIL"
                            entry["logically_equivalent"] = "no"
                        else:
                            entry["sat_check_status"] = "PASS"
                            entry["logically_equivalent"] = "yes"
                    except Exception:
                        entry["sat_check_status"] = "ERROR"
                        entry["logically_equivalent"] = "unknown"
                else:
                    entry["sat_check_status"] = "SKIPPED"

                # Cleanup preprocessed file
                if not self.keep_dimacs and path.isfile(target_path):
                    try:
                        remove(target_path)
                    except Exception:
                        pass

                results.append(entry)

                if self.progress_bar:
                    self.progress_bar.next()

        if self.progress_bar:
            self.progress_bar.finish()
            print()

        if self.summarizer:
            self.summarizer.run(results)

        if self.writer:
            self.writer.fieldnames = [
                "dimacs",
                "preprocessor_name",
                "preprocessor_time",
                "logically_equivalent",
                "count_check_status",
                "sat_check_status",
            ]
            self.writer.writeheader()
            self.writer.writerows(results)

        return results
