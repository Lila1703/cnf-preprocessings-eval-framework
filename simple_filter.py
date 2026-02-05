#!/usr/bin/env python3
from subprocess import check_output, STDOUT
import sys

dimacs = "../Benchmarks_Top30/automotive/automotive2/Knüppel2017-2_1.dimacs"

# Get raw PMC output
output = check_output(f"./preprocessors/pmc -vivification {dimacs}", 
                     shell=True, stderr=STDOUT, timeout=60)
output_str = output.decode('utf-8', errors='replace')

# Just filter: remove WARNING line, keep everything else
lines = output_str.split('\n')
filtered_lines = []
for line in lines:
    if not line.startswith('WARNING:'):
        filtered_lines.append(line)

# Write to file
with open('/tmp/pmc_simple_filter.dimacs', 'w') as f:
    f.write('\n'.join(filtered_lines))

print("Saved to /tmp/pmc_simple_filter.dimacs")

# Count lines
clause_lines = [l for l in filtered_lines if l.strip() and not l.startswith('c') and not l.startswith('p')]
print(f"Clause lines: {len(clause_lines)}")
