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
    
class BoundsConsistencyElimination(ExecutablePreprocessor):
    """A preprocessor that applies bounded consistency elimination (BCE).

    For details about BCE see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-ee -no-probe -bce -dimacs={target} {source}"
    name = "BoundsConsistencyElimination"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class XorReasoning(ExecutablePreprocessor):
    """A preprocessor that applies XOR reasoning.

    For details about XOR reasoning see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -dimacs={target} {source}"
    name = "XorReasoning"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class FourierMotzkin(ExecutablePreprocessor):
    """A preprocessor that applies Fourier-Motzkin reasoning.

    For details about Fourier-Motzkin reasoning see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -dimacs={target} {source}"
    name = "FourierMotzkin"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class DensePreprocessor(ExecutablePreprocessor):
    """A preprocessor that applies dense preprocessing.

    For details about dense preprocessing see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -dimacs={target} {source}"
    name = "DensePreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class Simplification(ExecutablePreprocessor):
    """A preprocessor that applies general simplification.

    For details about simplification see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -dimacs={target} {source}"
    name = "Simplification"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class UnhidingPreprocessor(ExecutablePreprocessor):
    """A preprocessor that applies unhiding.

    For details about unhiding see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -unhide -no-bve -no-bce -no-ee -no-probe -dimacs={target} {source}"
    name = "UnhidingPreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class StochasticLocalSearch(ExecutablePreprocessor):
    """A preprocessor that applies stochastic local search.

    For details about SLS see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -sls -dimacs={target} {source}"
    name = "StochasticLocalSearch"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class SymmetryDetection(ExecutablePreprocessor):
    """A preprocessor that applies symmetry detection and breaking.

    For details about symmetry detection see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -symm -dimacs={target} {source}"
    name = "SymmetryDetection"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class RewritingPreprocessor(ExecutablePreprocessor):
    """A preprocessor that applies rewriting.

    For details about rewriting see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -rew -dimacs={target} {source}"
    name = "RewritingPreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class BoundedVariableAddition(ExecutablePreprocessor):
    """A preprocessor that applies bounded variable addition (BVA).

    For details about BVA see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -bva -dimacs={target} {source}"
    name = "BoundedVariableAddition"

    def get_factor_of_number_of_solutions(self, output):
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
        
        # Get original variable count for header adjustment
        original_var_count = None
        try:
            with open(source, 'r') as f:
                for line in f:
                    if line.startswith('p'):
                        parts = line.split()
                        if len(parts) >= 3:
                            original_var_count = int(parts[2])
                        break
        except Exception:
            pass
        
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

                # If this is SharpSatPreprocessor, adjust the header to use original var count
                # This helps SharpSat process preprocessed files consistently
                preprocessor_input = current_source
                if preprocessor.name == "SharpSatPreprocessor" and current_source != source and original_var_count:
                    adjusted_path = f"{target}.{unique}.adjusted"
                    if _set_header_to_max_var(current_source, adjusted_path, original_var_count):
                        temp_files.append(adjusted_path)
                        preprocessor_input = adjusted_path

                step_factor = preprocessor.run(preprocessor_input, out_path, timeout)

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

def _set_header_to_max_var(input_file, output_file, target_var_count=None):
    """Set the header to use target_var_count (or max var if not specified).
    This helps SharpSat process preprocessed files consistently.
    """
    try:
        comments = []
        clauses = []
        max_var = 0
        
        # Read file
        with open(input_file, 'r') as f:
            for line in f:
                if line.startswith('c'):
                    comments.append(line)
                elif line.startswith('p'):
                    continue
                elif line.strip():
                    clauses.append(line)
                    literals = [int(x) for x in line.split()]
                    for lit in literals:
                        if lit != 0:
                            max_var = max(max_var, abs(lit))
        
        # Use target_var_count if provided, otherwise use max_var
        header_vars = target_var_count if target_var_count else max_var
        
        # Write output with adjusted header
        with open(output_file, 'w') as f:
            # Write comments
            for comment in comments:
                f.write(comment)
            
            # Write new header
            f.write(f"p cnf {header_vars} {len(clauses)}\n")
            
            # Write clauses as-is
            for clause in clauses:
                f.write(clause)
        
        return True
    except Exception:
        return False


def _renumber_variables_in_dimacs(input_file, output_file):
    """Renumber variables in a DIMACS file to be 1, 2, 3, ..., N.
    This ensures all variables are contiguous and properly ordered.
    Returns True on success, False on failure.
    """
    try:
        var_map = {}
        next_id = 1
        max_var = 0
        clauses = []
        comments = []
        
        # First pass: scan file to build variable mapping
        with open(input_file, 'r') as f:
            for line in f:
                if line.startswith('c'):
                    comments.append(line)
                elif line.startswith('p'):
                    continue
                elif line.strip():
                    literals = [int(x) for x in line.split()]
                    for lit in literals:
                        if lit == 0:
                            continue
                        abs_var = abs(lit)
                        if abs_var not in var_map:
                            var_map[abs_var] = next_id
                            next_id += 1
                        max_var = max(max_var, abs_var)
                    clauses.append(line)
        
        # Write output with renumbered variables
        with open(output_file, 'w') as f:
            # Write comments
            for comment in comments:
                f.write(comment)
            
            # Write new header
            num_vars = len(var_map)
            num_clauses = len(clauses)
            f.write(f"p cnf {num_vars} {num_clauses}\n")
            
            # Write renumbered clauses
            for clause_line in clauses:
                literals = [int(x) for x in clause_line.split()]
                new_literals = []
                for lit in literals:
                    if lit == 0:
                        new_literals.append('0')
                    else:
                        sign = 1 if lit > 0 else -1
                        new_lit = sign * var_map[abs(lit)]
                        new_literals.append(str(new_lit))
                
                f.write(' '.join(new_literals) + '\n')
        
        return True
    except Exception:
        return False            
