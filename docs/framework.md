# Framework

This file describes the architecture of the framework.

## Solvers

Solvers are implemented as subclasses of the `ExecutableSolver` class. This class defines two methods:

- `run(self, input, timeout=None)` which runs the solver on the file `input`. The optional `timeout` specifies a timeout in seconds after which the solver process should be terminated. The return value of `run` is the number of solutions found by the solver or `None` if either the timeout was triggered or the solver doesn't return the number of solutions.
- `get_number_of_solutions(self, output)` which given the output of the solver should return the number of solutions found. This method is used internally.

To integrate a solver into the framework, add a subclass of `ExecutableSolver`, set the class variable `command_line` to a shell command that calls your solver and implement the `get_number_of_solutions` function like in the following example:

```python
class MySolver(ExecutableSolver):
	# The framework will automatically replace "{input}" 
    # with the correct file when calling your solver
    command_line = "./mysolver {input}" 

    # The name of your solver, this should generally match the class name.
    name = "MySolver"

    # This function should return the number of
    # solutions given the output of your solver.
    # It can usually be implemented using a regular expression.
    def get_number_of_solutions(self, output):
        found = search("#SOLUTIONS: (\\d+)", output)
        if found:
            return int(found.group(1))

``` 

## Preprocessors

Preprocessors are implemented as subclasses of the `Preprocessor` class. This class has a single function:

- `run(self, source, target, timeout=None)` which runs the preprocessor, reading the input from `source` and writing the output to `target`. The optional `timeout` specifies a timeout after which the preprocessor process is terminated. This function returns the factor by which the preprocessor changed the number of solutions or `None` if this factor cannot be determined.

The easiest way to integrate a new preprocessor into the framework is to implement a subclass of `ExecutablePreprocessor`:

```python
class MyPreprocessor(ExecutablePreprocessor):
	# The framework will automatically replace "{source}" and
    # {target} with the correct file names when calling your solver.
    command_line = "./mypreprocessor {source} {target}"

    # The name of your preprocessor, this should generally match the class name.
    name = "MyPreprocessor"

    # The factor by which the number of solutions changed.
    # Multiplying this factor with the new number of solutions
    # should result in the original number of solutions.

    # This can be implemented as `return 1`
    # (if the preprocessor doesn't change the number of solutions).

    # For an example of a preprocessor that changes the number of solutions
    # see `EquivalentLiteralElimination`.
    def get_factor_of_number_of_solutions(self, output):
        return 1

```

## Summarizer

The `Summarizer` class is responsible for summarizing the results and printing them on the command line. It serves three purposes:

- Compare the number of solutions of all solvers without preprocessors and issue a warning if they disagree.
- Compare the number of solutions of all preprocessors for each solver and issue a warning if they disagree.
- Summarize the results and print a table containing the summarized results.

## ResultWriter

The `ResultWriter` class is responsible for writing the full results into a file. Its interface consists of the two functions `writeheader` and `writerows`. This interface is intentionally modelled after the interface of `csv.DictWriter`, such that it can be replaced easily by any other class implementing this interface including a `csv.DictWriter`.

The output of `ResultWriter` is a comma-separated values (CSV) file with the following format:

```
Model,Sol1NoPre,SOl1Pre1,Sol1Pre2,Sol1Pre3,Sol2NoPre,....
Model1,Rep1;Rep2;Rep3;...,Rep1;Rep2;.... 
```

For each model a single line is added to the output and each solver-preprocessor combination has a column. Each cell is therefore defined by a model-solver-preprocessor combination and contains a semicolon-separated list of runs.
