from itertools import groupby
from csv import writer


class ResultWriter:
    def __init__(self, file, _, flush_every=10, write_every=10):
        self.file = file
        self.writer = writer(file)
        self.write_headers = False
        self.fieldnames = None
        self.headers = None
        self.flush_every = flush_every
        self._rows_since_flush = 0
        self.write_every = write_every
        self._row_buffer = []

    def _maybe_flush(self, count):
        if not self.file or not self.flush_every:
            return
        self._rows_since_flush += count
        if self._rows_since_flush >= self.flush_every:
            self.file.flush()
            self._rows_since_flush = 0

    def _write_buffered(self):
        if not self._row_buffer:
            return
        self.writer.writerows(self._row_buffer)
        self._maybe_flush(len(self._row_buffer))
        self._row_buffer = []

    def flush(self):
        if self.fieldnames:
            self._write_buffered()
        if self.file:
            self.file.flush()
            self._rows_since_flush = 0

    def writeheader(self):
        self.write_headers = True

    def writerows(self, results):
        # If benchmarker set `fieldnames`, write one CSV row per result dict
        # using that order. This gives a simple table with one run per row and
        # the exact fields specified by `benchmarker`.
        if self.fieldnames:
            # Sort by dimacs, then preprocessor, then solver
            results = sorted(results, key=lambda x: (x.get("dimacs", ""), x.get("preprocessor_name", ""), x.get("solver_name", "")))
            if self.write_headers:
                self.writer.writerow(self.fieldnames)
                self.write_headers = False
            for run in results:
                row = []
                for f in self.fieldnames:
                    v = run.get(f, "")
                    if f == "solutions_preserved":
                        if v is True:
                            v = "yes"
                        elif v is False:
                            v = "no"
                        else:
                            v = "unknown"
                    row.append(v)
                self._row_buffer.append(row)
                if len(self._row_buffer) >= self.write_every:
                    self._write_buffered()
            return

        # Fallback: original compact format (one row per DIMACS, columns are
        # solver+preprocessor and cells contain semicolon-separated runtimes).
        if self.write_headers or self.headers is None:
            headers = ["Model"]
            for ((solver, preprocessor), _) in groupby(
                results, key=lambda x: (x["solver_name"], x["preprocessor_name"])
            ):
                headers.append(solver + preprocessor)
            self.headers = headers
            if self.write_headers:
                self.writer.writerow(headers)
                self.write_headers = False
        else:
            headers = self.headers

        results.sort(key=lambda x: x["dimacs"])
        rows_written = 0
        for (dimacs, data) in groupby(results, key=lambda x: x["dimacs"]):
            data = list(data)
            row = [dimacs]
            for solver_preprocessor in headers[1:]:
                cell = ""
                for run in data:
                    if (
                        run["solver_name"] + run["preprocessor_name"]
                        == solver_preprocessor
                    ):
                        cell += str(run["solver_time"] + run["preprocessor_time"]) + ";"
                cell = cell[:-1]
                row.append(cell)

            self.writer.writerow(row)
            rows_written += 1
        if rows_written:
            self._maybe_flush(rows_written)
