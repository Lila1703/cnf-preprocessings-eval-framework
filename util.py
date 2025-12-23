import os.path as path
from os import makedirs

def get_comments_string(input_path):
    with open(input_path, 'r') as file:
        comments = []
        for line in file:
            if line.startswith("c"):
                comments.append(line)
            else:
                break
    return ''.join(comments)


def preprend_content(part_to_prepent, input_path):
    with open(input_path, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(part_to_prepent + original_content)


def get_temp_dimacs_path(original_dimacs, preprocessor_name, keep_dimacs = False):
    if not keep_dimacs:
        return 'temp.dimacs'
    makedirs('preprocessed_dimacs', exist_ok=True)
    return path.join('preprocessed_dimacs', f'{preprocessor_name}-{path.basename(original_dimacs)}')


def fix_pcnf_header_to_original(original_dimacs, target_dimacs):
    """Ensure the 'p cnf' header in target_dimacs uses the variable count
    from original_dimacs and the correct clause count computed from target_dimacs.
    This avoids changes in declared variable count by preprocessors which can
    alter solver counting (e.g., dropping unused variable indices).
    """
    # Read original variable count
    orig_vars = None
    with open(original_dimacs, 'r') as f:
        for line in f:
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 3 and parts[0] == 'p' and parts[1] == 'cnf':
                    try:
                        orig_vars = int(parts[2])
                    except Exception:
                        orig_vars = None
                    break

    if orig_vars is None:
        return

    # Read target and count clauses (non-comment non-empty non-p lines)
    with open(target_dimacs, 'r') as f:
        lines = f.readlines()

    clause_lines = [l for l in lines if l.strip() and not l.startswith('c') and not l.startswith('p')]
    clause_count = len(clause_lines)

    # Replace or insert p cnf header as first non-comment line
    out_lines = []
    header_written = False
    for l in lines:
        if not header_written and l.strip():
            if l.startswith('c'):
                out_lines.append(l)
                continue
            # write new p cnf header
            out_lines.append(f"p cnf {orig_vars} {clause_count}\n")
            header_written = True
            # if the original first non-comment line was a p-line, skip it
            if l.startswith('p'):
                continue
            else:
                out_lines.append(l)
        else:
            out_lines.append(l)

    # If file was empty or contained only comments, ensure header exists
    if not header_written:
        out_lines.insert(0, f"p cnf {orig_vars} {clause_count}\n")

    with open(target_dimacs, 'w') as f:
        f.writelines(out_lines)
    
