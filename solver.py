from subprocess import check_output, STDOUT, CalledProcessError, TimeoutExpired
from re import search
from shlex import split


class ExecutableSolver:
    """Base class for all solvers.

    To define a new solver, define a subclass of this class and set
    the `command_line` class variable to command that calls your solver.
    For example:

    command_line = "./solvers/my_solver --input={input}"

    The parameter `{input}` will automatically be replaced by the
    correct file name when using the solver.

    You need to furthermore implement the function `get_number_of_solutions`
    that given the output of your solver returns the number of solutions.
    """

    def run(self, input, timeout=None):
        """Runs this solver on the file `input`.
        Returns the number of solutions the solver found."""
        try:
            command = split(self.command_line.format(input=input))
            output = check_output(command, stderr=STDOUT, timeout=timeout)
        except CalledProcessError as e:
            output = e.output
        except TimeoutExpired as e:
            return None
        return self.get_number_of_solutions(str(output))

    def get_number_of_solutions(self, output):
        """Returns the number of solutions the solver found."""
        ...


class SharpSat(ExecutableSolver):
    """The sharpSAT solver.

    See https://sites.google.com/site/marcthurley/sharpsat
    """

    command_line = "./solvers/sharpSAT {input}"
    name = "SharpSat"

    def get_number_of_solutions(self, output):
        found = search("# solutions \\\\n(\\d+)\\\\n# END", output)
        if found:
            return int(found.group(1))


class SharpSatWithoutBuiltinPreprocessor(ExecutableSolver):
    """The sharpSAT solver without the built in preprocessor.

    See https://sites.google.com/site/marcthurley/sharpsat
    """

    command_line = "./solvers/sharpSAT -noPP {input}"
    name = "SharpSatWithoutBuiltinPreprocessor"

    def get_number_of_solutions(self, output):
        found = search("# solutions \\\\n(\\d+)\\\\n# END", output)
        if found:
            return int(found.group(1))


class DSharp(ExecutableSolver):
    """The dsharp solver.

    See https://github.com/QuMuLab/dsharp
    """

    command_line = "./solvers/dsharp {input}"
    name = "DSharp"

    def get_number_of_solutions(self, output):
        found = search("#SAT \\(full\\):   \\\\t\\\\t(\\d+)", output)
        if found:
            return int(found.group(1))


class CountAntom(ExecutableSolver):
    """The countAntom solver.

    See https://projects.informatik.uni-freiburg.de/projects/countantom
    """

    command_line = "./solvers/countAntom {input}"
    name = "CountAntom"

    def get_number_of_solutions(self, output):
        found = search("c model count\\.*: (\\d+)", output)
        if found:
            return int(found.group(1))


class D4(ExecutableSolver):
    """The d4 solver.

    See http://www.cril.univ-artois.fr/kc/d4.html
    """

    command_line = "./solvers/d4 {input}"
    name = "D4"

    def get_number_of_solutions(self, output):
        found = search("s (\\d+)", output)
        if found:
            return int(found.group(1))


class BddMiniSat(ExecutableSolver):
    """The BDD-Minisat solver.

    See http://www.sd.is.uec.ac.jp/toda/code/cnf2obdd.html
    """

    command_line = "./solvers/bdd_minisat_all_static {input}"
    name = "BddMiniSat"

    def get_number_of_solutions(self, output):
        found = search("SAT \\(full\\)\\s+:\\s+(\\d+)", output)
        if found:
            return int(found.group(1))


class Ganak(ExecutableSolver):
    """The ganak solver.

    See https://github.com/meelgroup/ganak
    """

    command_line = "./solvers/ganak {input}"
    name = "Ganak"

    def get_number_of_solutions(self, output):
        found = search("s mc (\\d+)", output)
        if found:
            return int(found.group(1))


class RelSat(ExecutableSolver):
    """The relsat solver.

    See https://code.google.com/archive/p/relsat/
    """

    command_line = "./solvers/relsat -#c {input}"
    name = "RelSat"

    def get_number_of_solutions(self, output):
        found = search("Number of solutions: (\\d+)", output)
        if found:
            return int(found.group(1))


class C2D(ExecutableSolver):
    """The c2d solver.

    See http://reasoning.cs.ucla.edu/c2d/
    """

    command_line = "./solvers/c2d_linux -count -in {input}"
    name = "C2D"

    def get_number_of_solutions(self, output):
        found = search("Counting...(\\d+)", output)
        if found:
            return int(found.group(1))
