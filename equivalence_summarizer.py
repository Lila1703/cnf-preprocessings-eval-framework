from tabulate import tabulate
from csv import writer
from itertools import groupby


class EquivalenceSummarizer:
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

    def groupby_preprocessor(self, results):
        results.sort(key=lambda x: x["preprocessor_name"])
        return groupby(results, key=lambda x: x["preprocessor_name"])

    def run(self, results):
        print("\nEquivalence Check Results:")
        table = []

        for (preprocessor_name, data) in self.groupby_preprocessor(results):
            data = list(data)
            
            # Calculate average preprocessing time
            avg_preprocessor_time = sum(x["preprocessor_time"] for x in data) / len(data)
            
            # Count different status values
            count_check_pass = sum(1 for x in data if x.get("count_check_status") == "PASS")
            count_check_fail = sum(1 for x in data if x.get("count_check_status") == "FAIL")
            count_check_unknown = sum(1 for x in data if x.get("count_check_status") in ["UNKNOWN", "SKIPPED", "ERROR", None])
            
            sat_check_pass = sum(1 for x in data if x.get("sat_check_status") == "PASS")
            sat_check_fail = sum(1 for x in data if x.get("sat_check_status") == "FAIL")
            sat_check_unknown = sum(1 for x in data if x.get("sat_check_status") in ["UNKNOWN", "SKIPPED", "ERROR", None])
            
            # Aggregate logically_equivalent
            # - "yes" if all entries are "yes"
            # - "no" if any entry is "no"
            # - "unknown" otherwise
            logical_values = [x.get("logically_equivalent") for x in data]
            normalized_logical = []
            for v in logical_values:
                if v is None:
                    normalized_logical.append("unknown")
                elif isinstance(v, bool):
                    normalized_logical.append("yes" if v else "no")
                else:
                    nv = str(v).strip().lower()
                    if nv not in ("yes", "no", "unknown"):
                        nv = "unknown"
                    normalized_logical.append(nv)
            
            if all(v == "yes" for v in normalized_logical):
                logically_equivalent = "yes"
            elif any(v == "no" for v in normalized_logical):
                logically_equivalent = "no"
            elif all(v in ("yes", "unknown") for v in normalized_logical) and any(v == "yes" for v in normalized_logical):
                logically_equivalent = "yes"
            else:
                logically_equivalent = "unknown"
            
            # Build status summary strings
            count_status_str = f"{count_check_pass}P/{count_check_fail}F/{count_check_unknown}U"
            sat_status_str = f"{sat_check_pass}P/{sat_check_fail}F/{sat_check_unknown}U"
            
            table.append([
                preprocessor_name,
                avg_preprocessor_time,
                logically_equivalent,
                count_status_str,
                sat_status_str,
            ])

        headers = [
            "Preprocessor",
            "Avg. preprocessing time",
            "Logically equivalent",
            "Count check (P/F/U)",
            "SAT check (P/F/U)",
        ]

        print(tabulate(table, headers=headers))

        # Write summary to CSV if requested
        if self.csv_writer:
            self.csv_writer.writerow(headers)
            for row in table:
                self.csv_writer.writerow(row)
            self.csv_file.close()
