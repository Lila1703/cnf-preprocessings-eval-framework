from subprocess import check_output, STDOUT, CalledProcessError, TimeoutExpired
from re import search
from shlex import split
from fractions import Fraction
from time import time
import os
from uuid import uuid4
from shutil import move


class Preprocessor:
    def run(self, source, target, timeout=None):
        """Runs this preprocessor on the file `source` producing the file `target`.
        Returns the factor by which the number of solutions is expected to differ
        or `None` if this factor cannot be determined."""
        ...


class ExecutablePreprocessor(Preprocessor):
    """Base class for all executable preprocessors.

    To define a new preprocessor, define a subclass of this class and set
    the `command_line` class variable to command that calls your preprocessor.
    For example:

    command_line = "./preprocessors/my_preprocessor --input={input} --output={input}"

    The parameters `{input}` and `{output}` will automatically be replaced by the
    correct file names when using the preprocessor.
    """

    def run(self, source, target, timeout=None):
        try:
            command = split(self.command_line.format(source=source, target=target))
            output = check_output(command, stderr=STDOUT, timeout=timeout)
        except CalledProcessError as e:
            output = e.output
        except TimeoutExpired:
            return None
        except OSError as e:
            # Executable couldn't be started (bad format, missing interpreter,
            # wrong architecture, or missing file). Return None to signal a
            # failure so callers can fall back to the original DIMACS.
            print(f"Preprocessor execution failed: {e}")
            return None
        return self.get_factor_of_number_of_solutions(str(output))

    def get_factor_of_number_of_solutions(self, output):
        """Returns the factor by which the number of solutions is expected to differ
        or `None` if this factor cannot be determined."""
        ...


class NoPreprocessor(ExecutablePreprocessor):
    """A preprocessor that doesn't change the input.

    This preprocessor simply copies the input to the output. It is implemented
    as a system call to `cp`. Because this preprocessing doesn't change the
    input, it will also not change the number of solutions.
    """

    command_line = "cp {source} {target}"
    name = "NoPreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class UnitPropagation(ExecutablePreprocessor):
    """A preprocessnor that applies unit propagation.

    For details about unit propagation see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -up -dimacs={target} {source}"
    name = "UnitPropagation"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class Subsumption(ExecutablePreprocessor):
    """A preprocessnor that applies subsumption.

    For details about subsumption see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -subsimp -dimacs={target} {source}"
    name = "Subsumption"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class EquivalentLiteralElimination(ExecutablePreprocessor):
    """A preprocessnor that applies equivalent literal elimination.

    For details about equivalent literal elimination see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-probe -ee -no-cp3_eagerGates -dimacs={target} {source}"
    name = "EquivalentLiteralElimination"

    def get_factor_of_number_of_solutions(self, output):
        found = search("(\\d+) ee-lits", output)
        if found:
            return Fraction(1, 2 ** int(found.group(1)))


class Probing(ExecutablePreprocessor):
    """A preprocessnor that applies probing.

    For details about probing see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -probe -dimacs={target} {source}"
    name = "Probing"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class HiddenTautologyElimination(ExecutablePreprocessor):
    """A preprocessnor that applies hidden tautology elimination.

    For details about hidden tautology elimination see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -hte -dimacs={target} {source}"
    name = "HiddenTautologyElimination"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class SharpSatPreprocessor(ExecutablePreprocessor):
    """A preprocessnor that applies the sharpsat preprocessor.

    For details about the sharpsat preprocessor see preprocessors.md.
    """

    command_line = "./preprocessors/sharpSATpp {source} {target}"
    name = "SharpSatPreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class BinaryResolution(ExecutablePreprocessor):
    """A preprocessnor that applies binary resolution

    For details about binary resolution see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -addRed2 -dimacs={target} {source}"
    name = "BinaryResolution"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class HyperBinaryResolution(ExecutablePreprocessor):
    """A preprocessnor that applies hyper binary resolution

    For details about hyper binary resolution see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -hbr -dimacs={target} {source}"
    name = "HyperBinaryResolution"

    def get_factor_of_number_of_solutions(self, output):
        return 1

# Added by Linus
class BoundedVariableElimination(ExecutablePreprocessor): 
    """A preprocessnor that applies bounded variable elimination

    For details about bounded variable elimination see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bce -no-ee -no-probe -bve -dimacs={target} {source}"
    name = "BoundedVariableElimination"

    def get_factor_of_number_of_solutions(self, output):
        # found = search("(\\d+) bve-lits", output)
        # if found:
        #     return Fraction(1, 2 ** int(found.group(1)))
        return 1
    
class VariableElimination(ExecutablePreprocessor):
    """A preprocessnor that applies variable elimination

    For details about variable elimination see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bce -no-ee -no-probe -ve -dimacs={target} {source}"
    name = "VariableElimination"

    def get_factor_of_number_of_solutions(self, output):
        # found = search("(\\d+) ve-lits", output)
        # if found:
        #     return Fraction(1, 2 ** int(found.group(1)))
        return 1

class PreprocessorSequence(Preprocessor):
    """A preprocessor that applies multiple given preprocessors in order."""

    def __init__(self, preprocessors):
        self.preprocessors = preprocessors
        self.name = (
            "Sequence (" + ", ".join(map(lambda x: x.name, self.preprocessors)) + ")"
        )

    def run(self, source, target, timeout=None):
        factor = 1
        # Use a unique temporary base to avoid clashes with other runs.
        unique = uuid4().hex
        temp_files = []
        current_source = source
        try:
            for i, preprocessor in enumerate(self.preprocessors):
                start = time()
                # determine intermediate path; last step writes to a temp file
                # and we rename it to `target` atomically at the end to avoid
                # exposing partially-written files.
                if i == len(self.preprocessors) - 1:
                    out_path = f"{target}.{unique}.final"
                else:
                    out_path = f"{target}.{unique}.step{i}"

                step_factor = preprocessor.run(current_source, out_path, timeout)

                if step_factor is None:
                    # On failure, ensure we don't leave partial final file
                    try:
                        if os.path.exists(out_path):
                            os.remove(out_path)
                    except Exception:
                        pass
                    return None

                factor *= step_factor
                length = time() - start
                if timeout:
                    timeout = timeout - length
                    if timeout <= 0:
                        return None

                temp_files.append(out_path)
                current_source = out_path

            # Move the final temporary file to the requested target atomically
            final_temp = temp_files[-1] if temp_files else None
            if final_temp and os.path.exists(final_temp):
                try:
                    # ensure target dir exists
                    targ_dir = os.path.dirname(target)
                    if targ_dir and not os.path.exists(targ_dir):
                        os.makedirs(targ_dir, exist_ok=True)
                    os.replace(final_temp, target)
                except Exception:
                    # fallback to move
                    try:
                        move(final_temp, target)
                    except Exception:
                        pass

            return factor
        finally:
            # Cleanup any leftover intermediate files (excluding the final target)
            try:
                for f in temp_files:
                    if f and os.path.exists(f):
                        # do not remove the final target (we moved it)
                        if os.path.abspath(f) == os.path.abspath(target):
                            continue
                        try:
                            os.remove(f)
                        except Exception:
                            pass
            except Exception:
                pass
