from itertools import groupby
from csv import writer


class ResultWriter:
    def __init__(self, file, _):
        self.file = file
        self.writer = writer(file)
        self.write_headers = False

    def writeheader(self):
        self.write_headers = True

    def writerows(self, results):
        if self.write_headers:
            headers = ["Model"]
            for ((solver, preprocessor), _) in groupby(
                results, key=lambda x: (x["solver_name"], x["preprocessor_name"])
            ):
                headers.append(solver + preprocessor)
            self.writer.writerow(headers)

        results.sort(key=lambda x: x["dimacs"])
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
