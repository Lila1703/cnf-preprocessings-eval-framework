# Benchmarking framework

## Installation

Run `pip install -r requirements.txt` to install all required python packages. You might need to install `libc6:i386` to run the 32-bit ELF-executable `c2d_linux`.

## Usage

Currently the following commands are implemented:

### Listing all solvers:
```
> python3 main.py solvers
The following solvers are registered:
SharpSat
SharpSatWithoutBuiltinPreprocessor
DSharp
CountAntom
D4
D4V2
BddMiniSat
Ganak
RelSat
C2D
```

### Listing all preprocessors:
```
> python3 main.py preprocessors
The following preprocessors are registered:
NoPreprocessor
UnitPropagation_cop
Subsumption_cop
EquivalentLiteralElimination_cop
Probing_cop
Probing2_cop
HiddenTautologyElimination_cop
SharpSatPreprocessor
BinaryResolution_cop
HyperBinaryResolution_cop
BoundedVariableElimination_cop
SymmetryDetection_cop
BoundedVariableAddition_cop
CoveredClauseElimination_cop
FourierMotzkin_cop
Simplification_cop
TernaryClauseResolution_cop
ResolutionAsymmetricTautologyElimination_cop
LiteralAddition_cop
EntailedRedundancyCheck_cop
ModularityBasedPreprocessing_cop
Vivification_cop
Vivification_d4
D4Basic_d4
Backbone_d4
OccurrenceElimination_d4
Combinaison2_d4
D4SharpEquiv_d4
D4Equiv_d4
OrGate_arjun
IrregularGateRemoval_arjun
ITEGateDetection_arjun
XorGateDetection_arjun
SBVA_arjun
BCE_arjun
RevBCE_arjun
Distill_arjun
Probe_arjun
BVEPresimplify_arjun
Simplification_arjun
PreBackbone_arjun
Autarkies_arjun
GaussianJordan_arjun
OracleSparsify_arjun
OracleVivification_arjun
OracleVivificationGetL_arjun
Iteration1_arjun
Iteration2_arjun
Vivification_pmc
Vivification_pmc2
Affine2_pmc
OrGate2_pmc
EquivalenceDetection_pmc
Backbone_pmc
LiteralElimination2_pmc
AddClause2_pmc
BlockedClauseElimination_maxpre
UnitPropagation_maxpre
BoundedVariableElimination_maxpre
Subsumption_maxpre
SelfSubsumingResolution_maxpre
SubsumedLabelElimination_maxpre
BinaryCoreRemoval_maxpre
BoundedVariableAddition_maxpre
GeneralizedSubsumedLabelElimination_maxpre
EquivalenceElimination_maxpre
Unhiding_maxpre
StructureLabeling_maxpre
FailedliteralProbing_maxpre
```

### Running benchmarks:
```
> python3 main.py run -s SharpSat countAntom -p UnitPropagation EquivalentLiteralElimination Probing HiddenTautologyElimination -d ./test/mbx.dimacs -n 1 -o output.csv
Benchmarking |##################################################| 10/10 - ETA: 0s

Results:
Solver      Preprocessor                    Avg. preprocessor time    Avg. solver time    Avg. total time    Avg. speedup    Percentage finished
----------  ----------------------------  ------------------------  ------------------  -----------------  --------------  ---------------------
CountAntom  HiddenTautologyElimination                  0.00597239            0.256424           0.262396        1.17773                     100
CountAntom  EquivalentLiteralElimination                0.0057683             0.296055           0.301823        1.02388                     100
CountAntom  NoPreprocessor                              0.00118518            0.307846           0.309031        1                           100
CountAntom  UnitPropagation                             0.00466013            0.311194           0.315854        0.9784                      100
CountAntom  Probing                                     0.00469875            0.334188           0.338887        0.911901                    100
SharpSat    EquivalentLiteralElimination                0.00536084            0.37582            0.381181        4.12769                     100
SharpSat    HiddenTautologyElimination                  0.00621486            1.08621            1.09243         1.44027                     100
SharpSat    NoPreprocessor                              0.00137925            1.57202            1.5734          1                           100
SharpSat    Probing                                     0.00488329            1.58532            1.5902          0.989433                    100
SharpSat    UnitPropagation                             0.00483203            1.64226            1.64709         0.955258                    100
```

The following options are supported:

- `-s`/`--solver` with a list of solvers to benchmark
- `-p`/`--preprocessor` with a list of preprocessors to benchmark (optional, default: only solvers are run) (Sequences of preprocessings possible with "preprocessing1 preprocessing2")
- `-d`/`--dimacs` with a list of files in DIMACS CNT format
- `-n`/`--number-of-executions` with the number of times the benchmark should be repeated (optional, default: 1)
- `-o`/`--output` with the file where the full results should be written to (optional, default: full results are discarded)
- `-sum`/`--summary` with the file where the summary should be written to (optional, default: `summary.csv` when provided without value)
- `-t`/`--timeout` with the timeout (in seconds) after which a solver/preprocessor should be terminated (optional, default: no timeout)
- `--mem-limit-mb` sets a per-process memory limit in megabytes for solver runs; if a solver exceeds the limit, it is terminated and the run is marked unfinished. Useful to prevent D4 (or others) from exhausting system RAM.
- `-k`/`--keep_dimacs` keeps generated intermediate DIMACS files
- `-c`/`--copy_comments` copies comments from original DIMACS into generated files
- `--nonopreprocessor` disables automatic inclusion of `NoPreprocessor` as baseline

The output on the command line will be a summary of the full results sorted by the average total time:

- `Avg. preprocessor time` is the time the preprocessor took to process the input file. Note that `NoPreprocessor` also has a nonzero preprocessor time, because like the preprocessors it needs to read an input file and write an output file.
- `Avg. solver time` is the time the solver took to solve the preprocessed input.
- `Avg. total time` is the sum of the preprocessor time and the solver time.
- `Avg. speedup` is the speedup compared to the run without the preprocessor.
- `Percentage finished` is the percentage of runs that didn't timeout

To compare solvers without preprocessors, simply omit the `-p`/`--preprocessor` option:

```
> python3 main.py run -s SharpSat countAntom -d ./test/mbx.dimacs -n 5
Benchmarking |##################################################| 10/10 - ETA: 0s

Results:
Solver      Preprocessor      Avg. preprocessor time    Avg. solver time    Avg. total time    Avg. speedup    Percentage finished
----------  --------------  ------------------------  ------------------  -----------------  --------------  ---------------------
CountAntom  NoPreprocessor                0.00132699            0.400248           0.401575               1                    100
SharpSat    NoPreprocessor                0.00140333            1.60714            1.60854                1                    100
```

### Checking equivalence or model-counts (`check`)

This framework provides a `check` command to verify whether a preprocessor
preserves logical equivalence or preserves the model count.

Examples:

- Run an equivalence check (SAT-based) using the default SAT solver:
```
./bin/python main.py check -p UnitPropagation -d test/mbx.dimacs
```

- Run a counting-based check using the configured counter (default: `d4`):
```
./bin/python main.py check -p UnitPropagation -d test/mbx.dimacs --counter SharpSat
```


Meaning of outputs:
- `PASS` — The check succeeded (no counterexample found for equivalence, or counts match).
- `FAIL` — A counterexample was found (or counts do not match).
- `UNKNOWN` — A timeout or unclear solver output prevented a definite answer.

Notes and flags:
- `-p`/`--preprocessor` : name of the preprocessor (or a quoted sequence to create a pipeline). Must be provided for `check`.
- `-d`/`--dimacs` : DIMACS files or directories to check.
- `-S`/`--sat-solver` : SAT solver command template used for SAT-based checking (default: `./solvers/MiniSat_v1.14_linux {input}`).
- `--counter` : name of the counting solver to use (default: `d4`). The name must match a solver class in `solver.py`.
- `-o`/`--output` : write full check results to CSV.
- `-sum`/`--summary` : write check summary CSV (default: `equivalence_summary.csv` when provided without value).
- `-t`/`--timeout` : timeout in seconds for solver/preprocessor runs.
- `--mem-limit-mb` : per-process memory cap (MB) applied to the counter solver.
- `-k`/`--keep_dimacs` : keeps generated intermediate DIMACS files.
- `-c`/`--copy_comments` : copies comments from original DIMACS into generated files.

### Summarizing Existing Benchmark Output (`summarize`)

Create a summary CSV from an existing benchmark result CSV:

```
python3 main.py summarize output.csv
```

Options:
- `input` : path to input CSV file (required).
- `-o`/`--output` : path to output summary CSV file (optional, default: `<input>_summary.csv`).
