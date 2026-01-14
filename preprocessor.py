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
    
class Subsumption2(ExecutablePreprocessor):
    """A preprocessnor that applies subsumption.

    For details about subsumption see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-pre -no-xor -no-fm -no-simplify -no-dense -no-bve -no-ee -no-bce -no-unhide -no-receive -no-rer-f -no-rer-l -no-revMin -no-updLearnAct -no-refConflict -no-r-dyn-bl -no-useIP -no-usePP -no-randInp -no-cp3_limited -subsimp -dimacs={target} {source}"
    name = "Subsumption2"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class EquivalentLiteralElimination(ExecutablePreprocessor):
    """A preprocessnor that applies equivalent literal elimination.

    For details about equivalent literal elimination see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-pre -no-xor -no-fm -no-simplify -no-dense -no-bve -ee -no-bce -no-unhide -no-receive -no-rer-f -no-rer-l -no-revMin -no-updLearnAct -no-refConflict -no-r-dyn-bl -no-useIP -no-usePP -no-randInp -no-cp3_limited -no-enabled_cp3  -dimacs={target} {source}"
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
        return 1
    
class BlockedClauseElimination(ExecutablePreprocessor):
    """A preprocessor that applies blocked clause elimination (BCE).

    For details about BCE see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-ee -no-probe -bce -dimacs={target} {source}"
    name = "BlockedClauseElimination"

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


class SymmetryDetection(ExecutablePreprocessor):
    """A preprocessor that applies symmetry detection and breaking.

    For details about symmetry detection see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -symm -dimacs={target} {source}"
    name = "SymmetryDetection"

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
    
class CoveredClauseElimination(ExecutablePreprocessor):
    """A preprocessor that applies covered clause elimination (CCE).


    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -cce -dimacs={target} {source}"
    name = "CoveredClauseElimination"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class ShufflePreprocessor(ExecutablePreprocessor):
    """A preprocessor that shuffles the formula before preprocessing.

    For details about shuffling see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -shuffle -dimacs={target} {source}"
    name = "ShufflePreprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class TernaryClauseResolution(ExecutablePreprocessor):
    """A preprocessor that applies ternary clause resolution.

    For details about ternary clause resolution see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -3resolve -dimacs={target} {source}"
    name = "TernaryClauseResolution"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class ResolutionAsymmetricTautologyElimination(ExecutablePreprocessor):
    """A preprocessor that applies resolution asymmetric tautology elimination (RATE).

    For details about RATE see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -rate -dimacs={target} {source}"
    name = "ResolutionAsymmetricTautologyElimination"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class LiteralAddition(ExecutablePreprocessor):
    """A preprocessor that applies literal addition (LA).

    For details about literal addition see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -la -dimacs={target} {source}"
    name = "LiteralAddition"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class ExperimentalSimplification(ExecutablePreprocessor):
    """A preprocessor that applies experimental simplification techniques.

    For details about experimental simplification see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -exp -dimacs={target} {source}"
    name = "ExperimentalSimplification"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class EntailedRedundancyCheck(ExecutablePreprocessor):
    """A preprocessor that checks for entailed redundancy during preprocessing.

    For details about entailed redundancy checking see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -ent -dimacs={target} {source}"
    name = "EntailedRedundancyCheck"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class ModularityBasedPreprocessing(ExecutablePreprocessor):
    """A preprocessor that applies modularity-based preprocessing.

    For details about modularity-based preprocessing see preprocessors.md.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-dense -no-simplify -no-unhide -no-bve -no-bce -no-ee -no-probe -modprep -dimacs={target} {source}"
    name = "ModularityBasedPreprocessing"

    def get_factor_of_number_of_solutions(self, output):
        return 1


class TestCoprocessor(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-simplify -no-dense -no-bve -no-ee -no-bce -no-unhide -dimacs={target} {source}"
    name = "TestCoprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class CoprocessorOff(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/coprocessor -no-pre -no-xor -no-fm -no-simplify -no-dense -no-bve -no-ee -no-bce -no-unhide -no-receive -no-rer-f -no-rer-l -no-revMin -no-updLearnAct -no-refConflict -no-r-dyn-bl -no-useIP -no-usePP -no-randInp -no-cp3_limited -no-enabled_cp3  -dimacs={target} {source}"
    name = "CoprocessorOff"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class CoprocessorSequence(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-simplify -no-dense -no-bve -no-ee -no-bce -no-unhide -hte -subsimp -ent -dimacs={target} {source}"
    name = "CoprocessorSequence"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class CoprocessorSequence2(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-fm -no-simplify -no-dense -no-bve -no-ee -no-bce -no-unhide -subsimp -ent -hte -dimacs={target} {source}"
    name = "CoprocessorSequence2"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class DefaultCoprocessor(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/coprocessor -no-xor -no-dense -no-unhide -no-bve -no-bce -no-ee -dimacs={target} {source}"
    name = "DefaultCoprocessor"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    

# D4v2 Preprocessors

class Vivification(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p vivification --target {target} --preproc-only 1"
    name = "Vivification"

    def get_factor_of_number_of_solutions(self, output):
        return 1

class D4Basic(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p basic --target {target} --preproc-only 1"
    name = "D4Basic"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class Backbone(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p backbone --target {target} --preproc-only 1"
    name = "Backbone"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class OccurrenceElimination(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p occElimination --target {target} --preproc-only 1"
    name = "OccurrenceElimination"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class Combinaison(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p combinaison --target {target} --preproc-only 1"
    name = "Combinaison"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class D4SharpEquiv(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p sharpEquiv --target {target} --preproc-only 1"
    name = "D4SharpEquiv"

    def get_factor_of_number_of_solutions(self, output):
        return 1
    
class D4Equiv(ExecutablePreprocessor):
    """A preprocessor that applies all default coprocessor simplifications.
    """

    command_line = "./preprocessors/d4v2_preproc -i {source} -p equiv --target {target} --preproc-only 1"
    name = "D4Equiv"

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
    def get_factor_of_number_of_solutions(self, output):
        return 1

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
         
